from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class BacklogItem(BaseModel):
    id: Optional[str] = None
    index: Optional[str] = None
    source: Optional[str] = None
    message: Optional[str] = None
    timestamp: Optional[str] = None


class ReplayInfo(BaseModel):
    timerange_start: Optional[str] = None
    timerange_end: Optional[str] = None
    query: Optional[str] = None
    streams: List[str] = Field(default_factory=list)
    filters: List[Dict[str, str]] = Field(default_factory=list)


class Event(BaseModel):
    id: Optional[str] = None
    source: Optional[str] = None
    message: Optional[str] = None
    priority: Optional[int] = None
    timestamp: Optional[str] = None
    timestamp_processing: Optional[str] = None
    timerange_start: Optional[str] = None
    timerange_end: Optional[str] = None

    origin_context: Optional[str] = None
    key: Optional[str] = None
    key_tuple: List[str] = Field(default_factory=list)

    streams: List[str] = Field(default_factory=list)
    source_streams: List[str] = Field(default_factory=list)

    fields: Dict[str, str] = Field(default_factory=dict)
    replay_info: Optional[ReplayInfo] = None


class WebhookPayload(BaseModel):
    event_definition_id: Optional[str] = None
    event_definition_type: Optional[str] = None
    event_definition_title: Optional[str] = None
    event_definition_description: Optional[str] = None
    job_definition_id: Optional[str] = None
    job_trigger_id: Optional[str] = None

    event: Event
    backlog: List[BacklogItem] = Field(default_factory=list)
