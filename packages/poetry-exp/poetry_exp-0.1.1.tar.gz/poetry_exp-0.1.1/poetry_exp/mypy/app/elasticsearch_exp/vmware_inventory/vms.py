# (C) Copyright 2020 Hewlett Packard Enterprise Development Company, L.P.

from app_catalog.es_data.common.constants import ANALYZER, ALIAS_VMS

MAPPING_URI = '/' + ALIAS_VMS

GET_ALL_PARAMS = [
    'name', 'moref', 'id', 'status',
    'state', 'tags', 'createdAt', 'updatedAt']

VMS_INDEX_MAPPING_DEFINITION = \
    {
        "properties": {
            "id": {
                "type": "keyword",
                "ignore_above": 36
            },
            "name": {
                "type": "text",
                "analyzer": ANALYZER,
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 255
                    }
                }
            },
            "moref": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 255
                    }
                }
            },
            "tags": {
                "properties": {
                    "id": {
                        "type": "keyword",
                        "ignore_above": 36
                    },
                    "name": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                }
            },
            "createdAt": {
                "type": "date"
            },
            "updatedAt": {
                "type": "date"
            }
        }
    }
