"""Interface wrapper for Utilities API."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, Iterator, List

from requests import Response, delete, get, post
from utility_api.models.endpoints.authorization import (
    Authorization,
    AuthorizationListing,
)
from utility_api.models.endpoints.bill import Bill, BillsListing
from utility_api.models.endpoints.form import Form
from utility_api.models.endpoints.interval import (
    DataPoint,
    Interval,
    IntervalsListing,
)
from utility_api.models.endpoints.meter import Meter

UTILITIES_API: str = "api"
UTILITIES_VERSION: str = "v2"


@dataclass
class UtilitiesService:
    """Integrations related to Utilities API."""

    utilities_token: str
    headers: Dict[str, str] = field(default_factory=dict)
    utilities_base_url: str = (
        f"https://utilityapi.com/{UTILITIES_API}/{UTILITIES_VERSION}"
    )

    def __post_init__(self) -> None:
        """Populate the headers dictionary."""
        authorization_key: str = "Authorization"
        if authorization_key not in self.headers:
            self.headers[authorization_key] = f"Bearer {self.utilities_token}"

    @property
    def utilities_forms_url(self) -> str:  # noqa: D102
        return f"{self.utilities_base_url}/forms"

    @property
    def utilities_authorizations_url(self) -> str:  # noqa: D102
        return f"{self.utilities_base_url}/authorizations"

    @property
    def utilities_meters_url(self) -> str:  # noqa: D102
        return f"{self.utilities_base_url}/meters"

    @property
    def utilities_bills_url(self) -> str:  # noqa: D102
        return f"{self.utilities_base_url}/bills"

    @property
    def utilities_intervals_url(self) -> str:  # noqa: D102
        return f"{self.utilities_base_url}/intervals"

    def create_new_form(self) -> Form:
        """Create a new form for authorizing a utilities customer.

        Returns:
            An authorization form
        """
        response: Response = post(f"{self.utilities_forms_url}", headers=self.headers)
        if response.status_code == 200:
            return Form.from_json(response.text)

    def get_form_by_uid(self, form_uid: str) -> Form:
        """Get an authorization form from a form UID.

        Args:
            form_uid: The UID of a form of interest

        Returns:
            The authorization form of the provided UID
        """
        response: Response = get(
            f"{self.utilities_forms_url}/{form_uid}", headers=self.headers
        )
        return Form.from_json(response.text)

    def get_authorizations_from_referral(
        self, referral_code: str, include_meters: bool
    ) -> List[Authorization]:
        """Get the client's authorization from a referral code.

        Args:
            referral_code: The referral code
            include_meters: Flag to include basic meter information

        Returns:
            A list of authorizations from the referral code
        """
        url = f"{self.utilities_authorizations_url}?referrals={referral_code}"
        if include_meters:
            url += "&include=meters"
        response: Response = get(url, headers=self.headers)
        listing = AuthorizationListing.from_json(response.text)
        authorizations: List[Authorization] = listing.authorizations
        return authorizations

    def list_all_authorizations(self) -> List[Authorization]:
        """List all authorizations available to the Utility API account.

        Returns:
            A list authorizations.
        """
        response: Response = get(
            f"{self.utilities_authorizations_url}", headers=self.headers
        )
        listing = AuthorizationListing.from_json(response.text)
        authorizations: List[Authorization] = listing.authorizations
        return authorizations

    def get_authorizations_by_uid(self, authorization_uid: str) -> List[Authorization]:
        """Get an authorization object from an authorization UID.

        Args:
            authorization_uid: The UID of the authorization of interest

        Returns:
            A list of authorizations from the provided uid
        """
        response: Response = get(
            f"{self.utilities_authorizations_url}/{authorization_uid}",
            headers=self.headers,
        )
        authorization = Authorization.from_json(response.text)
        authorizations: List[Authorization] = []
        for referral_code in authorization.referrals:
            authorizations.extend(
                self.get_authorizations_from_referral(
                    referral_code, include_meters=True
                )
            )
        return authorizations

    def get_meter_by_uid(self, meter_uid: str) -> Meter:
        """Get a meter object from a meter UID.

        Args:
            meter_uid: The UID of the meter of interest

        Returns:
            The Meter object of the provided UID
        """
        response: Response = get(
            f"{self.utilities_meters_url}/{meter_uid}", headers=self.headers
        )
        if response.status_code == 200:
            return Meter.from_json(response.text)

    def trigger_historical_collection(self, meter_uids: list[str]) -> None:
        """Trigger the collection of historical data for list of meters.

        Args:
            meter_uids: A list of meter UIDs
        """
        response: Response = post(
            f"{self.utilities_meters_url}/historical-collection",
            headers=self.headers,
            data=json.dumps({"meters": meter_uids}),
        )
        if response.status_code == 200:
            print("Successfully triggered historical collection.")
        else:
            print("Historical collection failed.")

    def delete_test_authorizations(self) -> None:
        """Delete authorizations from the Demo account."""
        test_authorization_uids = [
            authorization.uid
            for authorization in self.list_all_authorizations()
            if authorization.is_test
        ]
        for authorization_uid in test_authorization_uids:
            response = delete(
                f"{self.utilities_authorizations_url}/{authorization_uid}",
                headers=self.headers,
            )
            print(response, response.text)

    def bills_by_meter_uid(self, meter_uid: str) -> Iterator[Bill]:
        """Collect the bills associated with a meter of interest.

        Args:
            meter_uid: The UID of the meter of interest

        Yields:
            A bill associated with the meter
        """
        response: Response = get(
            f"{self.utilities_bills_url}?meters={meter_uid}", headers=self.headers
        )
        listing = BillsListing.from_json(response.text)
        for bill in listing.bills:
            yield bill

    def intervals_by_meter_uid(self, meter_uid: str) -> Iterator[Interval]:
        """Collect the intervals associated with a meter of interest.

        Args:
            meter_uid: The UID of the meter of interest

        Yields:
            An interval associated with the meter
        """
        response: Response = get(
            f"{self.utilities_intervals_url}?meters={meter_uid}", headers=self.headers
        )
        listing = IntervalsListing.from_json(response.text)
        for interval in listing.intervals:
            yield interval

    def datapoints_from_interval_readings_by_meter_uid(
        self, meter_uid: str
    ) -> Iterator[DataPoint]:
        """Get the interval readings from a meter of interest.

        Args:
            meter_uid: The UID of the meter of interest

        Yields:
            A datapoint for the meter of interest
        """
        for interval in self.intervals_by_meter_uid(meter_uid):
            for reading in interval.readings:
                for datapoint in reading.datapoints_with_reading_metadata():
                    yield datapoint
