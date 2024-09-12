default_procedures = [
    {
        "id": 1,
        "subject": {
            "id": 1
        },
        "collection_result": "success",
        "collectors": [
            {
                "id": 1567,
                "sequence": 1,
                "collection_result": "filled",
            },
            {
                "id": 1568,
                "sequence": 2,
                "collection_result": "filled",
            },
            {
                "id": 1569,
                "sequence": 3,
                "collection_result": "filled",
            }
        ]
    },
    {
        "id": 2,
        "subject": {
            "id": 1
        },
        "collection_result": "partial_success",
        "collectors": [
            {
                "id": 1570,
                "sequence": 1,
                "collection_result": "filled",
            },
            {
                "id": 1571,
                "sequence": 2,
                "collection_result": "partial_filled",
            },
            {
                "id": 1572,
                "sequence": 3,
                "collection_result": "filled",
            }
        ]
    },
    {
        "id": 3,
        "subject": {
            "id": 2
        },
        "collection_result": "failure",
        "collectors": [
            {
                "id": 1573,
                "sequence": 1,
                "collection_result": "filled",
            },
            {
                "id": 1574,
                "sequence": 2,
                "collection_result": "filled",
            },
            {
                "id": 1575,
                "sequence": 3,
                "collection_result": "empty",
            },
            {
                "id": 1576,
                "sequence": 4,
                "collection_result": "partial_filled",
            }

        ]
    }
]


class LisServiceObjectNotFound(Exception):
    pass


class LisService:
    def __init__(self, procedures: list = None):
        procedure_list = procedures or default_procedures
        self.procedure_map = {procedure["id"]: procedure for procedure in procedure_list}

    def get_procedure_by_collector_id(self, collector_id: int) -> dict:
        for procedure in self.procedure_map.values():
            for collector in procedure["collectors"]:
                if collector["id"] == collector_id:
                    return procedure

        raise LisServiceObjectNotFound("Procedure not found")

    def get_procedure_by_procedure_id(self, procedure_id: int) -> dict:
        if procedure_id not in self.procedure_map:
            raise LisServiceObjectNotFound("Procedure not found")

        return self.procedure_map[procedure_id]

    def update_procedure(self, procedure_id: int, procedure: dict) -> dict:
        if procedure_id not in self.procedure_map:
            raise LisServiceObjectNotFound("Procedure not found")

        self.procedure_map[procedure_id] = procedure
        return self.procedure_map[procedure_id]


lis_service = LisService()
