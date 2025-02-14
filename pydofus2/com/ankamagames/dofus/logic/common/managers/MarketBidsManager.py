from collections import defaultdict
from typing import TYPE_CHECKING, Generator, List, Optional, Tuple

from prettytable import PrettyTable

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemType import ItemType
from pydofus2.com.ankamagames.dofus.logic.common.managers.MarketBid import MarketBid
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseInListUpdatedMessage import (
        ExchangeBidHouseInListUpdatedMessage,
    )
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseItemAddOkMessage import (
        ExchangeBidHouseItemAddOkMessage,
    )
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidHouseItemRemoveOkMessage import (
        ExchangeBidHouseItemRemoveOkMessage,
    )
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeBidPriceForSellerMessage import (
        ExchangeBidPriceForSellerMessage,
    )
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeStartedBidSellerMessage import (
        ExchangeStartedBidSellerMessage,
    )
    from pydofus2.com.ankamagames.dofus.network.messages.game.inventory.exchanges.ExchangeTypesItemsExchangerDescriptionForUserMessage import (
        ExchangeTypesItemsExchangerDescriptionForUserMessage,
    )


class MarketBidsManager:
    """Manages market state and rule tracking"""

    MAX_LISTING_DAYS = 28
    MAX_LISTING_HOURS = MAX_LISTING_DAYS * 24
    MAX_LISTING_SECONDS = MAX_LISTING_HOURS * 3600

    def __init__(self):
        self._logger = Logger()

        # Market rules from seller descriptor
        self.max_delay = self.MAX_LISTING_SECONDS
        self.tax_percentage: int = None
        self.max_item_level: int = None
        self.max_item_count: int = None
        self.allowed_types: List[int] = []
        self.valid_quantities: List[int] = []
        self.npc_id: Optional[int] = None

        # Use defaultdict for nested dictionaries
        self.min_price = defaultdict(lambda: defaultdict(int))  # gid -> quantity -> price
        self.avg_prices = defaultdict(lambda: defaultdict(int))  # gid -> quantity -> avg price

        # Nested defaultdict for listings
        self._bids = defaultdict(lambda: defaultdict(list[MarketBid]))  # gid -> quantity -> listings

    def get_all_bids(self) -> Generator[MarketBid, None, None]:
        """Get all active bids across all items"""
        for gid_listings in self._bids.values():
            for quantity_listings in gid_listings.values():
                for bid in quantity_listings:
                    yield bid

    def get_all_updatable_bids(self, min_age: int) -> List[MarketBid]:
        """Get all updatable listings sorted by highest price first"""
        updatable = [bid for bid in self.get_all_bids() if bid.age_hours >= min_age]
        return sorted(updatable, key=lambda x: x.price, reverse=True)

    def get_remaining_sell_slots(self) -> int:
        """
        Get number of remaining sell slots
        Returns: Number of available listing slots
        """
        total_listings = sum(
            len(quantity_listings)
            for gid_listings in self._bids.values()
            for quantity_listings in gid_listings.values()
        )

        return max(0, self.max_item_count - total_listings)

    def init_from_seller_descriptor(self, msg: "ExchangeStartedBidSellerMessage") -> None:
        """Initialize market rules and our listings from seller descriptor"""
        descriptor = msg.sellerDescriptor
        self.tax_percentage = descriptor.taxPercentage
        self.max_item_level = descriptor.maxItemLevel
        self.max_item_count = descriptor.maxItemPerAccount
        self.allowed_types = list(descriptor.types)
        self.valid_quantities = list(descriptor.quantities)
        self.npc_id = descriptor.npcContextualId

        for item in msg.objectsInfos:
            listing = MarketBid.from_message(item, self.max_delay)
            self._add_bid(listing)

        # Display the bids table after initialization if there are any bids
        self.display_market_rules()
        self.display_current_bids()

    def _add_bid(self, listing: MarketBid) -> None:
        """
        Track one of our listings and maintain sorted order

        Args:
            listing (MarketBid): The new market bid to track
        """
        # Initialize nested defaultdict structure if needed
        bids_for_quantity = self._bids[listing.item_gid][listing.quantity]

        # Remove existing bid with same UID if it exists
        for i, existing_bid in enumerate(bids_for_quantity):
            if existing_bid.uid == listing.uid:
                bids_for_quantity.pop(i)
                break

        # Add the new/updated bid
        bids_for_quantity.append(listing)
        # Sort bids (assuming MarketBid implements comparison methods)
        self._bids[listing.item_gid][listing.quantity].sort()

    def handle_search_result(self, msg: "ExchangeTypesItemsExchangerDescriptionForUserMessage") -> None:
        """Handle market price information from item search"""
        if not msg.itemTypeDescriptions:
            self._logger.debug(f"No price data for item {msg.objectGID}")
            return

        first_item = msg.itemTypeDescriptions[0]

        # Track initial market state
        for i, quantity in enumerate(self.valid_quantities):
            if i < len(first_item.prices):
                self.min_price[msg.objectGID][quantity] = first_item.prices[i]

        self._logger.debug(
            f"Received search result for item {msg.objectGID}: {list(self.min_price[msg.objectGID].values())}"
        )
        return msg.objectGID

    def get_bid_by_uid(self, uid: int) -> Optional[MarketBid]:
        """Find a listing by its unique identifier across all items"""
        for gid_listings in self._bids.values():
            for quantity_listings in gid_listings.values():
                for listing in quantity_listings:
                    if listing.uid == uid:
                        return listing
        return None

    def handle_market_update(self, msg: "ExchangeBidHouseInListUpdatedMessage") -> List[Tuple[int, int, int]]:
        """Track market price changes with ownership awareness"""
        changes = []

        for i, quantity in enumerate(self.valid_quantities):
            if i < len(msg.prices):
                old_price = self.min_price[msg.objectGID][quantity]
                new_price = msg.prices[i]

                if old_price != new_price:
                    KernelEventsManager().send(
                        KernelEvent.AssetPriceChanged, msg.objectGID, quantity, old_price, new_price
                    )
                    our_min = self.get_bid_min_price(msg.objectGID, quantity)
                    if our_min and new_price < our_min:
                        KernelEventsManager().send(
                            KernelEvent.NewMarketLow, msg.objectGID, quantity, old_price, new_price
                        )
                    self.min_price[msg.objectGID][quantity] = new_price
                    changes.append((msg.objectGID, quantity, old_price, new_price))
                    self._logger.info(
                        f"Market price changed: gid={msg.objectGID} qty={quantity} " f"old={old_price} new={new_price}"
                    )

        return changes

    def handle_price_info(self, msg: "ExchangeBidPriceForSellerMessage") -> None:
        """Update current market prices"""
        self._logger.debug(
            f"Updating prices for item {msg.genericId}: min={msg.minimalPrices}, avg={msg.averagePrice}"
        )

        for i, quantity in enumerate(self.valid_quantities):
            if i < len(msg.minimalPrices):
                self.min_price[msg.genericId][quantity] = msg.minimalPrices[i]
                self.avg_prices[msg.genericId][quantity] = msg.averagePrice * quantity

                KernelEventsManager().send(
                    KernelEvent.MarketPriceUpdate,
                    msg.genericId,
                    quantity,
                    self.min_price[msg.genericId][quantity],
                    self.avg_prices[msg.genericId][quantity],
                )

    def _remove_bid(self, uid: int) -> Optional["MarketBid"]:
        """Remove one of our listings when sold/removed"""
        listing = self.get_bid_by_uid(uid)
        if not listing:
            return None

        quantity_listings = self._bids[listing.item_gid][listing.quantity]
        for i, l in enumerate(quantity_listings):
            if l.uid == uid:
                removed = quantity_listings.pop(i)
                self._logger.info(
                    f"Removed listing: uid={removed.uid} "
                    f"gid={removed.item_gid} qty={removed.quantity} "
                    f"price={removed.price} age={removed.age_hours:.1f}h"
                )

                # Clean up empty containers
                if not quantity_listings:
                    del self._bids[listing.item_gid][listing.quantity]
                    if not self._bids[listing.item_gid]:
                        del self._bids[listing.item_gid]

                return removed
        return None

    def handle_bid_removed(self, msg: "ExchangeBidHouseItemRemoveOkMessage") -> Optional["MarketBid"]:
        """
        Process listing removal
        Returns removed listing if found
        """
        listing = self._remove_bid(msg.sellerId)
        if listing:
            self._logger.debug(
                f"Listing removed: {listing.uid} "
                f"({listing.quantity}x @ {listing.price}, "
                f"age={listing.age // 60}min)"
            )
        return listing

    def handle_bid_added(self, msg: "ExchangeBidHouseItemAddOkMessage") -> "MarketBid":
        """Track when one of our listings is added"""
        listing = MarketBid.from_message(msg.itemInfo, self.max_delay)
        self._add_bid(listing)
        self._logger.info(
            f"Added listing: uid={listing.uid} "
            f"gid={listing.item_gid} qty={listing.quantity} "
            f"price={listing.price} age={60 * listing.age_hours:.1f}min"
        )
        current_min = self.min_price[msg.itemInfo.objectGID][listing.quantity]
        if current_min == 0 or listing.price <= current_min:
            self.min_price[msg.itemInfo.objectGID][listing.quantity] = listing.price
            self._logger.debug(
                f"Our new listing is lowest price for item {msg.itemInfo.objectGID} "
                f"{listing.quantity}x at {listing.price}"
            )

        return listing

    def get_bids(self, item_gid: int, quantity: int) -> List[MarketBid]:
        """Get sorted listings for quantity"""
        return self._bids[item_gid][quantity]

    def calculate_tax(self, price: int) -> int:
        """Calculate tax amount for given price"""
        return (price * self.tax_percentage) // 100

    def get_bids_older_than(self, item_gid: int, quantity: int, hours: float) -> List[MarketBid]:
        """Get listings older than specified hours"""
        min_age = int(hours * 3600)
        listings = self.get_bids(item_gid, quantity)

        return sorted([l for l in listings if l.age >= min_age], key=lambda x: x.age, reverse=True)

    def get_bid_min_price(self, item_gid: int, quantity: int) -> Optional[int]:
        """Get our lowest listing price for given item and quantity"""
        listings = self.get_bids(item_gid, quantity)
        if not listings:
            return None
        return min(listing.price for listing in listings)

    def get_updatable_bids(
        self, item_gid: int, quantity: int, min_hours: float, min_price_ratio: float
    ) -> Tuple[List[MarketBid], Optional[int], Optional[str]]:
        """Get updatable listings sorted by highest price first, then oldest first"""
        target_price, error = self.get_sell_price(item_gid, quantity, min_price_ratio)
        if error:
            self._logger.debug(f"Cannot get updatable listings: {error}")
            return [], target_price, error

        min_age = int(min_hours * 3600)
        listings = self.get_bids(item_gid, quantity)

        # Update any listings above the target price
        updatable = [listing for listing in listings if listing.age >= min_age and listing.price > target_price]

        if updatable:
            updatable.sort()  # Sort by highest price first, then oldest
            self._logger.debug(
                f"Found updatable listings: gid={item_gid} qty={quantity} "
                f"count={len(updatable)} highest_price={updatable[0].price} "
                f"target_price={target_price} oldest_age={60 * updatable[0].age_hours:.1f}min"
            )

        return updatable, target_price, None

    def get_sell_price(
        self, item_gid: int, quantity: int, min_price_ratio: float
    ) -> Tuple[Optional[int], Optional[str]]:
        """Calculate optimal price based on market conditions and minimum acceptable price"""
        market_price = self.min_price[item_gid][quantity]
        avg_price = self.avg_prices[item_gid][quantity]

        if not market_price or not avg_price:
            return None, f"Unable to get market prices"

        min_acceptable = int(avg_price * min_price_ratio)
        our_min = self.get_bid_min_price(item_gid, quantity)

        self._logger.debug(f"Market state: gid={item_gid} qty={quantity} " f"market={market_price} our_min={our_min}")

        if market_price < min_acceptable:
            return None, f"Market price {market_price} below minimum {min_acceptable}"

        if our_min and our_min <= market_price:
            return our_min, None

        # We don't own minimum - try to beat it
        target_price = max(min_acceptable, market_price - 1)
        self._logger.debug(f"undercutting {market_price} to {target_price}")
        return target_price, None

    def count_bids_le_market(self, item_gid: int, quantity: int) -> int:
        market_price = self.min_price[item_gid][quantity]
        listings = self.get_bids(item_gid, quantity)
        return sum(1 for listing in listings if listing.price <= market_price)

    def display_market_rules(self) -> None:
        """Display market characteristics in a formatted table"""
        market_info = PrettyTable()
        market_info.field_names = ["Market Characteristics", "Value"]
        market_info.align["Market Characteristics"] = "l"  # Left align first column
        market_info.align["Value"] = "r"  # Right align second column
        market_info.add_row(["Maximum Items", f"{self.max_item_count:,}"])
        market_info.add_row(["Maximum Item Level", f"{self.max_item_level:,}"])
        market_info.add_row(["Tax Percentage", f"{self.tax_percentage}%"])
        market_info.add_row(["Maximum Listing Duration", f"{self.MAX_LISTING_DAYS} days"])
        market_info.add_row(["Available Slots", f"{self.get_remaining_sell_slots():,}"])

        # Add allowed quantities in a readable format
        quantities_str = ", ".join(str(q) for q in sorted(self.valid_quantities))
        market_info.add_row(["Valid Quantities", quantities_str])

        # Add allowed types in a readable format
        type_names = []
        for type_id in self.allowed_types:
            try:
                item_type = ItemType.getItemTypeById(int(type_id))
                if item_type:
                    type_names.append(item_type.name)
            except:
                type_names.append(f"Type {type_id}")
        types_str = ", ".join(type_names)
        market_info.add_row(["Allowed Types", types_str[:50] + "..." if len(types_str) > 50 else types_str])

        market_info.border = True
        market_info.title = "Market Rules"

        self._logger.info("\nMarket Status Report")
        self._logger.info("=" * 80)
        self._logger.info(f"\n{market_info}")

    def display_current_bids(self) -> None:
        """Display current bids in a formatted table"""
        bids_table = PrettyTable()
        bids_table.field_names = ["Item Name", "Item GID", "Type", "Quantity", "Price", "Market Min", "Time Left"]
        bids_table.align = "r"  # Right align all columns
        bids_table.align["Item Name"] = "l"  # Left align item names
        bids_table.align["Type"] = "l"  # Left align type names

        total_value = 0
        total_tax = 0

        for item_gid in self._bids:
            for quantity in self._bids[item_gid]:
                market_min = self.min_price[item_gid][quantity]
                for bid in self._bids[item_gid][quantity]:
                    item = Item.getItemById(item_gid)
                    total_value += bid.price
                    total_tax += self.calculate_tax(bid.price)

                    # Color coding for price comparison
                    price_str = f"{bid.price:,}"
                    if bid.price <= market_min:
                        price_str = f"{price_str}*"  # Mark lowest price

                    bids_table.add_row(
                        [
                            item.name,
                            item_gid,
                            item.type.name,
                            f"{quantity:,}",
                            price_str,
                            f"{market_min:,}" if market_min > 0 else "N/A",
                            bid.formatted_time_left,
                        ]
                    )

        # Add summary row
        if self._bids:
            bids_table.add_row(["TOTALS", "", "", "", f"{total_value:,}", "", f"Tax: {total_tax:,}"])

        # Sort by price and quantity
        bids_table.sortby = "Price"
        bids_table.title = "Current Market Bids"

        if self._bids:
            self._logger.info(f"\n{bids_table}")
            self._logger.info("\n* Indicates lowest price on market")
        else:
            self._logger.info("\nNo active listings")
