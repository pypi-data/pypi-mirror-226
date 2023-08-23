import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.schedule_w_jobs_args import ScheduleWJobsArgs
from ..models.schedule_w_jobs_extra_perms import ScheduleWJobsExtraPerms
from ..models.schedule_w_jobs_jobs_item import ScheduleWJobsJobsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScheduleWJobs")


@attr.s(auto_attribs=True)
class ScheduleWJobs:
    """
    Attributes:
        path (str):
        edited_by (str):
        edited_at (datetime.datetime):
        schedule (str):
        timezone (str):
        enabled (bool):
        script_path (str):
        is_flow (bool):
        extra_perms (ScheduleWJobsExtraPerms):
        email (str):
        args (Union[Unset, ScheduleWJobsArgs]):
        error (Union[Unset, str]):
        on_failure (Union[Unset, str]):
        jobs (Union[Unset, List[ScheduleWJobsJobsItem]]):
    """

    path: str
    edited_by: str
    edited_at: datetime.datetime
    schedule: str
    timezone: str
    enabled: bool
    script_path: str
    is_flow: bool
    extra_perms: ScheduleWJobsExtraPerms
    email: str
    args: Union[Unset, ScheduleWJobsArgs] = UNSET
    error: Union[Unset, str] = UNSET
    on_failure: Union[Unset, str] = UNSET
    jobs: Union[Unset, List[ScheduleWJobsJobsItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        schedule = self.schedule
        timezone = self.timezone
        enabled = self.enabled
        script_path = self.script_path
        is_flow = self.is_flow
        extra_perms = self.extra_perms.to_dict()

        email = self.email
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        error = self.error
        on_failure = self.on_failure
        jobs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.jobs, Unset):
            jobs = []
            for jobs_item_data in self.jobs:
                jobs_item = jobs_item_data.to_dict()

                jobs.append(jobs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "schedule": schedule,
                "timezone": timezone,
                "enabled": enabled,
                "script_path": script_path,
                "is_flow": is_flow,
                "extra_perms": extra_perms,
                "email": email,
            }
        )
        if args is not UNSET:
            field_dict["args"] = args
        if error is not UNSET:
            field_dict["error"] = error
        if on_failure is not UNSET:
            field_dict["on_failure"] = on_failure
        if jobs is not UNSET:
            field_dict["jobs"] = jobs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        schedule = d.pop("schedule")

        timezone = d.pop("timezone")

        enabled = d.pop("enabled")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        extra_perms = ScheduleWJobsExtraPerms.from_dict(d.pop("extra_perms"))

        email = d.pop("email")

        _args = d.pop("args", UNSET)
        args: Union[Unset, ScheduleWJobsArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = ScheduleWJobsArgs.from_dict(_args)

        error = d.pop("error", UNSET)

        on_failure = d.pop("on_failure", UNSET)

        jobs = []
        _jobs = d.pop("jobs", UNSET)
        for jobs_item_data in _jobs or []:
            jobs_item = ScheduleWJobsJobsItem.from_dict(jobs_item_data)

            jobs.append(jobs_item)

        schedule_w_jobs = cls(
            path=path,
            edited_by=edited_by,
            edited_at=edited_at,
            schedule=schedule,
            timezone=timezone,
            enabled=enabled,
            script_path=script_path,
            is_flow=is_flow,
            extra_perms=extra_perms,
            email=email,
            args=args,
            error=error,
            on_failure=on_failure,
            jobs=jobs,
        )

        schedule_w_jobs.additional_properties = d
        return schedule_w_jobs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
