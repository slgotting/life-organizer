from typing import Dict, List


PlayerName = str
GroupName = str
Email = str

GroupMember = Dict[str, str]
GroupData = Dict[GroupName, Dict[str, List[GroupMember]]]
