# Volumes (volumes)[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#volumes-volumes)

A volume is a detachable block storage device similar to a USB hard drive. You can attach a volume to one instance at a time.

The `snapshot_id` and `source_volid` parameters specify the ID of the snapshot or volume from which this volume originates. If the volume was not created from a snapshot or source volume, these values are null.

When you create, list, update, or delete volumes, the possible status values are:

**Volume statuses**

| Status            | Description                                            |
| ----------------- | ------------------------------------------------------ |
| creating          | The volume is being created.                           |
| available         | The volume is ready to attach to an instance.          |
| reserved          | The volume is reserved for attaching or shelved.       |
| attaching         | The volume is attaching to an instance.                |
| detaching         | The volume is detaching from an instance.              |
| in-use            | The volume is attached to an instance.                 |
| maintenance       | The volume is locked and being migrated.               |
| deleting          | The volume is being deleted.                           |
| awaiting-transfer | The volume is awaiting for transfer.                   |
| error             | A volume creation error occurred.                      |
| error_deleting    | A volume deletion error occurred.                      |
| backing-up        | The volume is being backed up.                         |
| restoring-backup  | A backup is being restored to the volume.              |
| error_backing-up  | A backup error occurred.                               |
| error_restoring   | A backup restoration error occurred.                   |
| error_extending   | An error occurred while attempting to extend a volume. |
| downloading       | The volume is downloading an image.                    |
| uploading         | The volume is being uploaded to an image.              |
| retyping          | The volume is changing type to another volume type.    |
| extending         | The volume is being extended.                          |

### List accessible volumes with details	GET		/v3/{project_id}/volumes/detail

Lists all Block Storage volumes, with details, that the project can access, since v3.31 if non-admin users specify invalid filters in the url, API will return bad request.

#### Response codes[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id81)

##### Success[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Success)

| Code       | Reason                  |
| ---------- | ----------------------- |
| `200 - OK` | Request was successful. |

##### Error[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Error)

| Code                | Reason                                   |
| ------------------- | ---------------------------------------- |
| `400 - Bad Request` | Some content in the request was invalid. |

#### Request[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id82)

| Name                   | In    | Type    | Description                                                  |
| ---------------------- | ----- | ------- | ------------------------------------------------------------ |
| project_id             | path  | string  | The UUID of the project in a multi-tenancy cloud.            |
| all_tenants (Optional) | query | string  | Shows details for all project. Admin only.                   |
| sort (Optional)        | query | string  | Comma-separated list of sort keys and optional sort directions in the form of < key > [: < direction > ]. A valid direction is `asc` (ascending) or `desc` (descending). |
| limit (Optional)       | query | integer | Requests a page size of items. Returns a number of items up to a limit value. Use the `limit` parameter to make an initial limited request and use the ID of the last-seen item from the response as the `marker` parameter value in a subsequent limited request. |
| offset (Optional)      | query | integer | Used in conjunction with `limit` to return a slice of items. `offset` is where to start in the list. |
| marker (Optional)      | query | string  | The ID of the last-seen item. Use the `limit` parameter to make an initial limited request and use the ID of the last-seen item from the response as the `marker` parameter value in a subsequent limited request. |
| with_count (Optional)  | query | boolean | Whether to show `count` in API response or not, default is `False`.**New in version 3.45** |

#### Response Parameters[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id83)

| Name                             | In   | Type    | Description                                                  |
| -------------------------------- | ---- | ------- | ------------------------------------------------------------ |
| migration_status                 | body | string  | The volume migration status.                                 |
| attachments                      | body | array   | Instance attachment information. If this volume is attached to a server instance, the attachments list includes the UUID of the attached server, an attachment UUID, the name of the attached host, if any, the volume UUID, the device, and the device UUID. Otherwise, this list is empty. |
| links                            | body | array   | The volume links.                                            |
| availability_zone (Optional)     | body | string  | The name of the availability zone.                           |
| os-vol-host-attr:host            | body | string  | Current back-end of the volume. Host format is `host@backend#pool`. |
| encrypted                        | body | boolean | If true, this volume is encrypted.                           |
| updated_at                       | body | string  | The date and time when the resource was updated.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. In the previous example, the offset value is `-05:00`.If the `updated_at` date and time stamp is not set, its value is `null`. |
| replication_status               | body | string  | The volume replication status.                               |
| snapshot_id (Optional)           | body | string  | To create a volume from an existing snapshot, specify the UUID of the volume snapshot. The volume is created in same availability zone and with same size as the snapshot. |
| id                               | body | string  | The UUID of the volume.                                      |
| size                             | body | integer | The size of the volume, in gibibytes (GiB).                  |
| user_id                          | body | string  | The UUID of the user.                                        |
| os-vol-tenant-attr:tenant_id     | body | string  | The project ID which the volume belongs to.                  |
| os-vol-mig-status-attr:migstat   | body | string  | The status of this volume migration (None means that a migration is not currently in progress). |
| metadata                         | body | object  | A `metadata` object. Contains one or more metadata key and value pairs that are associated with the volume. |
| status                           | body | string  | The volume status.                                           |
| volume_image_metadata (Optional) | body | object  | List of image metadata entries. Only included for volumes that were created from an image, or from a snapshot of a volume originally created from an image. |
| description                      | body | string  | The volume description.                                      |
| multiattach                      | body | boolean | If true, this volume can attach to more than one instance.   |
| source_volid (Optional)          | body | string  | The UUID of the source volume. The API creates a new volume with the same size as the source volume unless a larger size is requested. |
| consistencygroup_id              | body | string  | The UUID of the consistency group.                           |
| os-vol-mig-status-attr:name_id   | body | string  | The volume ID that this volume name on the back- end is based on. |
| name                             | body | string  | The volume name.                                             |
| bootable                         | body | string  | Enables or disables the bootable attribute. You can boot an instance from a bootable volume. |
| created_at                       | body | string  | The date and time when the resource was created.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. |
| volumes                          | body | array   | A list of `volume` objects.                                  |
| volume_type                      | body | string  | The associated volume type for the volume.                   |
| volumes_links (Optional)         | body | array   | The volume links.                                            |
| count (Optional)                 | body | integer | The total count of requested resource before pagination is applied.**New in version 3.45** |

#### Response Example[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id86)

```
{
    "volumes": [
        {
            "migration_status": null,
            "attachments": [
                {
                    "server_id": "f4fda93b-06e0-4743-8117-bc8bcecd651b",
                    "attachment_id": "3b4db356-253d-4fab-bfa0-e3626c0b8405",
                    "host_name": null,
                    "volume_id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                    "device": "/dev/vdb",
                    "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38"
                }
            ],
            "links": [
                {
                    "href": "http://23.253.248.171:8776/v3/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                    "rel": "self"
                },
                {
                    "href": "http://23.253.248.171:8776/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                    "rel": "bookmark"
                }
            ],
            "availability_zone": "nova",
            "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1",
            "encrypted": false,
            "replication_status": "disabled",
            "snapshot_id": null,
            "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
            "size": 2,
            "user_id": "32779452fcd34ae1a53a797ac8a1e064",
            "os-vol-tenant-attr:tenant_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",
            "os-vol-mig-status-attr:migstat": null,
            "metadata": {
                "readonly": false,
                "attached_mode": "rw"
            },
            "status": "in-use",
            "description": null,
            "multiattach": true,
            "source_volid": null,
            "consistencygroup_id": null,
            "os-vol-mig-status-attr:name_id": null,
            "name": "test-volume-attachments",
            "bootable": "false",
            "created_at": "2015-11-29T03:01:44.000000",
            "volume_type": "lvmdriver-1"
        },
        {
            "migration_status": null,
            "attachments": [],
            "links": [
                {
                    "href": "http://23.253.248.171:8776/v3/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/173f7b48-c4c1-4e70-9acc-086b39073506",
                    "rel": "self"
                },
                {
                    "href": "http://23.253.248.171:8776/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/173f7b48-c4c1-4e70-9acc-086b39073506",
                    "rel": "bookmark"
                }
            ],
            "availability_zone": "nova",
            "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1",
            "encrypted": false,
            "replication_status": "disabled",
            "snapshot_id": null,
            "id": "173f7b48-c4c1-4e70-9acc-086b39073506",
            "size": 1,
            "user_id": "32779452fcd34ae1a53a797ac8a1e064",
            "os-vol-tenant-attr:tenant_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",
            "os-vol-mig-status-attr:migstat": null,
            "metadata": {},
            "status": "available",
            "volume_image_metadata": {
                "kernel_id": "8a55f5f1-78f7-4477-8168-977d8519342c",
                "checksum": "eb9139e4942121f22bbc2afc0400b2a4",
                "min_ram": "0",
                "ramdisk_id": "5f6bdf8a-92db-4988-865b-60bdd808d9ef",
                "disk_format": "ami",
                "image_name": "cirros-0.3.4-x86_64-uec",
                "image_id": "b48c53e1-9a96-4a5a-a630-2e74ec54ddcc",
                "container_format": "ami",
                "min_disk": "0",
                "size": "25165824"
            },
            "description": "",
            "multiattach": false,
            "source_volid": null,
            "consistencygroup_id": null,
            "os-vol-mig-status-attr:name_id": null,
            "name": "test-volume",
            "bootable": "true",
            "created_at": "2015-11-29T02:25:18.000000",
            "volume_type": "lvmdriver-1"
        }
    ],
    "volumes_links": [{
        "href": "https://158.69.65.111/volume/v3/4ad9f06ab8654e40befa59a2e7cac86d/volumes/detail?limit=1&marker=3b451d5d-9358-4a7e-a746-c6fd8b0e1462",
        "rel": "next"
    }],
    "count": 10
}
```

### Create a volume	 POST	/v3/{project_id}/volumes

To create a bootable volume, include the UUID of the image from which you want to create the volume in the `imageRef` attribute in the request body.

Preconditions

- You must have enough volume storage quota remaining to create a volume of size requested.

Asynchronous Postconditions

- With correct permissions, you can see the volume status as `available` through API calls.
- With correct access, you can see the created volume in the storage system that OpenStack Block Storage manages.

Troubleshooting

- If volume status remains `creating` or shows another error status, the request failed. Ensure you meet the preconditions then investigate the storage back end.
- Volume is not created in the storage system that OpenStack Block Storage manages.
- The storage node needs enough free storage space to match the size of the volume creation request.

#### Response codes[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id87)

##### Success[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Success)

| Code             | Reason                                                  |
| ---------------- | ------------------------------------------------------- |
| `202 - Accepted` | Request is accepted, but processing may take some time. |

#### Request[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id88)

| Name                                  | In   | Type    | Description                                                  |
| ------------------------------------- | ---- | ------- | ------------------------------------------------------------ |
| project_id                            | path | string  | The UUID of the project in a multi-tenancy cloud.            |
| volume                                | body | object  | A `volume` object.                                           |
| size                                  | body | integer | The size of the volume, in gibibytes (GiB).                  |
| availability_zone (Optional)          | body | string  | The name of the availability zone.                           |
| source_volid (Optional)               | body | string  | The UUID of the source volume. The API creates a new volume with the same size as the source volume unless a larger size is requested. |
| description (Optional)                | body | string  | The volume description.                                      |
| multiattach (Optional)                | body | boolean | To enable this volume to attach to more than one server, set this value to `true`. Default is `false`. Note that support for multiattach volumes depends on the volume type being used. See [valid boolean values](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#valid-boolean-values) |
| snapshot_id (Optional)                | body | string  | To create a volume from an existing snapshot, specify the UUID of the volume snapshot. The volume is created in same availability zone and with same size as the snapshot. |
| backup_id (Optional)                  | body | string  | The UUID of the backup.**New in version 3.47**               |
| name (Optional)                       | body | string  | The volume name.                                             |
| imageRef (Optional)                   | body | string  | The UUID of the image from which you want to create the volume. Required to create a bootable volume. |
| volume_type (Optional)                | body | string  | The volume type (either name or ID). To create an environment with multiple-storage back ends, you must specify a volume type. Block Storage volume back ends are spawned as children to `cinder- volume`, and they are keyed from a unique queue. They are named `cinder- volume.HOST.BACKEND`. For example, `cinder-volume.ubuntu.lvmdriver`. When a volume is created, the scheduler chooses an appropriate back end to handle the request based on the volume type. Default is `None`. For information about how to use volume types to create multiple- storage back ends, see [Configure multiple-storage back ends](https://docs.openstack.org/cinder/latest/admin/blockstorage-multi-backend.html). |
| metadata (Optional)                   | body | object  | One or more metadata key and value pairs to be associated with the new volume. |
| consistencygroup_id                   | body | string  | The UUID of the consistency group.                           |
| OS-SCH-HNT:scheduler_hints (Optional) | body | object  | The dictionary of data to send to the scheduler.             |

#### Request Example[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id90)

```
{
    "volume": {
        "size": 10,
        "availability_zone": null,
        "source_volid": null,
        "description": null,
        "multiattach": false,
        "snapshot_id": null,
        "backup_id": null,
        "name": null,
        "imageRef": null,
        "volume_type": null,
        "metadata": {},
        "consistencygroup_id": null
    },
    "OS-SCH-HNT:scheduler_hints": {
        "same_host": [
            "a0cf03a5-d921-4877-bb5c-86d26cf818e1",
            "8c19174f-4220-44f0-824a-cd1eeef10287"
        ]
    }
}
```

#### Response Parameters[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id91)

| Name                         | In   | Type    | Description                                                  |
| ---------------------------- | ---- | ------- | ------------------------------------------------------------ |
| migration_status             | body | string  | The volume migration status.                                 |
| attachments                  | body | array   | Instance attachment information. If this volume is attached to a server instance, the attachments list includes the UUID of the attached server, an attachment UUID, the name of the attached host, if any, the volume UUID, the device, and the device UUID. Otherwise, this list is empty. |
| links                        | body | array   | The volume links.                                            |
| availability_zone (Optional) | body | string  | The name of the availability zone.                           |
| encrypted                    | body | boolean | If true, this volume is encrypted.                           |
| updated_at                   | body | string  | The date and time when the resource was updated.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. In the previous example, the offset value is `-05:00`.If the `updated_at` date and time stamp is not set, its value is `null`. |
| replication_status           | body | string  | The volume replication status.                               |
| snapshot_id (Optional)       | body | string  | To create a volume from an existing snapshot, specify the UUID of the volume snapshot. The volume is created in same availability zone and with same size as the snapshot. |
| id                           | body | string  | The UUID of the volume.                                      |
| size                         | body | integer | The size of the volume, in gibibytes (GiB).                  |
| user_id                      | body | string  | The UUID of the user.                                        |
| metadata                     | body | object  | A `metadata` object. Contains one or more metadata key and value pairs that are associated with the volume. |
| status                       | body | string  | The volume status.                                           |
| description                  | body | string  | The volume description.                                      |
| multiattach                  | body | boolean | If true, this volume can attach to more than one instance.   |
| source_volid (Optional)      | body | string  | The UUID of the source volume. The API creates a new volume with the same size as the source volume unless a larger size is requested. |
| volume                       | body | object  | A `volume` object.                                           |
| consistencygroup_id          | body | string  | The UUID of the consistency group.                           |
| name                         | body | string  | The volume name.                                             |
| bootable                     | body | string  | Enables or disables the bootable attribute. You can boot an instance from a bootable volume. |
| created_at                   | body | string  | The date and time when the resource was created.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. |
| volume_type                  | body | string  | The associated volume type for the volume.                   |

#### Response Example[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id94)

```
{
    "volume": {
        "status": "creating",
        "migration_status": null,
        "user_id": "0eea4eabcf184061a3b6db1e0daaf010",
        "attachments": [],
        "links": [
            {
                "href": "http://23.253.248.171:8776/v3/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                "rel": "self"
            },
            {
                "href": "http://23.253.248.171:8776/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                "rel": "bookmark"
            }
        ],
        "availability_zone": "nova",
        "bootable": "false",
        "encrypted": false,
        "created_at": "2015-11-29T03:01:44.000000",
        "description": null,
        "updated_at": null,
        "volume_type": "lvmdriver-1",
        "name": "test-volume-attachments",
        "replication_status": "disabled",
        "consistencygroup_id": null,
        "source_volid": null,
        "snapshot_id": null,
        "multiattach": false,
        "metadata": {},
        "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
        "size": 2
    }
}
```

### List accessible volumes		GET		/v3/{project_id}/volumes

Lists summary information for all Block Storage volumes that the project can access, since v3.31 if non-admin users specify invalid filters in the url, API will return bad request.

#### Response codes[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id95)

##### Success[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Success)

| Code       | Reason                  |
| ---------- | ----------------------- |
| `200 - OK` | Request was successful. |

##### Error[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Error)

| Code                | Reason                                   |
| ------------------- | ---------------------------------------- |
| `400 - Bad Request` | Some content in the request was invalid. |

#### Request[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id96)

| Name                   | In    | Type    | Description                                                  |
| ---------------------- | ----- | ------- | ------------------------------------------------------------ |
| project_id             | path  | string  | The UUID of the project in a multi-tenancy cloud.            |
| all_tenants (Optional) | query | string  | Shows details for all project. Admin only.                   |
| sort (Optional)        | query | string  | Comma-separated list of sort keys and optional sort directions in the form of < key > [: < direction > ]. A valid direction is `asc` (ascending) or `desc` (descending). |
| limit (Optional)       | query | integer | Requests a page size of items. Returns a number of items up to a limit value. Use the `limit` parameter to make an initial limited request and use the ID of the last-seen item from the response as the `marker` parameter value in a subsequent limited request. |
| offset (Optional)      | query | integer | Used in conjunction with `limit` to return a slice of items. `offset` is where to start in the list. |
| marker (Optional)      | query | string  | The ID of the last-seen item. Use the `limit` parameter to make an initial limited request and use the ID of the last-seen item from the response as the `marker` parameter value in a subsequent limited request. |
| with_count (Optional)  | query | boolean | Whether to show `count` in API response or not, default is `False`.**New in version 3.45** |

#### Response Parameters[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id97)

| Name                     | In   | Type    | Description                                                  |
| ------------------------ | ---- | ------- | ------------------------------------------------------------ |
| volumes                  | body | array   | A list of `volume` objects.                                  |
| id                       | body | string  | The UUID of the volume.                                      |
| links                    | body | array   | The volume links.                                            |
| name                     | body | string  | The volume name.                                             |
| volumes_links (Optional) | body | array   | The volume links.                                            |
| count (Optional)         | body | integer | The total count of requested resource before pagination is applied.**New in version 3.45** |

#### Response Example[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id98)

```
{
    "volumes": [
        {
            "id": "45baf976-c20a-4894-a7c3-c94b7376bf55",
            "links": [
                {
                    "href": "http://localhost:8776/v3/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/45baf976-c20a-4894-a7c3-c94b7376bf55",
                    "rel": "self"
                },
                {
                    "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/45baf976-c20a-4894-a7c3-c94b7376bf55",
                    "rel": "bookmark"
                }
            ],
            "name": "vol-004"
        },
        {
            "id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
            "links": [
                {
                    "href": "http://localhost:8776/v3/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "rel": "self"
                },
                {
                    "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "rel": "bookmark"
                }
            ],
            "name": "vol-003"
        }
    ],
    "volumes_links": [{
        "href": "https://158.69.65.111/volume/v3/4ad9f06ab8654e40befa59a2e7cac86d/volumes/detail?limit=1&marker=3b451d5d-9358-4a7e-a746-c6fd8b0e1462",
        "rel": "next"
    }],
    "count": 10
}
```

### Show a volume’s details		GET		/v3/{project_id}/volumes/{volume_id}

Preconditions

- The volume must exist.

#### Response codes[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id99)

##### Success[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Success)

| Code       | Reason                  |
| ---------- | ----------------------- |
| `200 - OK` | Request was successful. |

#### Request[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id100)

| Name       | In   | Type   | Description                                       |
| ---------- | ---- | ------ | ------------------------------------------------- |
| project_id | path | string | The UUID of the project in a multi-tenancy cloud. |
| volume_id  | path | string | The UUID of the volume.                           |

#### Response Parameters[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id101)

| Name                             | In   | Type    | Description                                                  |
| -------------------------------- | ---- | ------- | ------------------------------------------------------------ |
| migration_status                 | body | string  | The volume migration status.                                 |
| attachments                      | body | array   | Instance attachment information. If this volume is attached to a server instance, the attachments list includes the UUID of the attached server, an attachment UUID, the name of the attached host, if any, the volume UUID, the device, and the device UUID. Otherwise, this list is empty. |
| links                            | body | array   | The volume links.                                            |
| availability_zone (Optional)     | body | string  | The name of the availability zone.                           |
| os-vol-host-attr:host            | body | string  | Current back-end of the volume. Host format is `host@backend#pool`. |
| encrypted                        | body | boolean | If true, this volume is encrypted.                           |
| updated_at                       | body | string  | The date and time when the resource was updated.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. In the previous example, the offset value is `-05:00`.If the `updated_at` date and time stamp is not set, its value is `null`. |
| replication_status               | body | string  | The volume replication status.                               |
| snapshot_id (Optional)           | body | string  | To create a volume from an existing snapshot, specify the UUID of the volume snapshot. The volume is created in same availability zone and with same size as the snapshot. |
| id                               | body | string  | The UUID of the volume.                                      |
| size                             | body | integer | The size of the volume, in gibibytes (GiB).                  |
| user_id                          | body | string  | The UUID of the user.                                        |
| os-vol-tenant-attr:tenant_id     | body | string  | The project ID which the volume belongs to.                  |
| os-vol-mig-status-attr:migstat   | body | string  | The status of this volume migration (None means that a migration is not currently in progress). |
| metadata                         | body | object  | A `metadata` object. Contains one or more metadata key and value pairs that are associated with the volume. |
| status                           | body | string  | The volume status.                                           |
| volume_image_metadata (Optional) | body | object  | List of image metadata entries. Only included for volumes that were created from an image, or from a snapshot of a volume originally created from an image. |
| description                      | body | string  | The volume description.                                      |
| multiattach                      | body | boolean | If true, this volume can attach to more than one instance.   |
| source_volid (Optional)          | body | string  | The UUID of the source volume. The API creates a new volume with the same size as the source volume unless a larger size is requested. |
| volume                           | body | object  | A `volume` object.                                           |
| consistencygroup_id              | body | string  | The UUID of the consistency group.                           |
| os-vol-mig-status-attr:name_id   | body | string  | The volume ID that this volume name on the back- end is based on. |
| name                             | body | string  | The volume name.                                             |
| bootable                         | body | string  | Enables or disables the bootable attribute. You can boot an instance from a bootable volume. |
| created_at                       | body | string  | The date and time when the resource was created.The date and time stamp format is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601):`CCYY-MM-DDThh:mm:ss±hh:mm `For example, `2015-08-27T09:49:58-05:00`.The `±hh:mm` value, if included, is the time zone as an offset from UTC. |
| volume_type                      | body | string  | The associated volume type for the volume.                   |
| service_uuid                     | body | string  | A unique identifier that’s used to indicate what node the volume-service for a particular volume is being serviced by. |
| shared_targets                   | body | boolean | An indicator whether the back-end hosting the volume utilizes shared_targets or not. Default=True. |

#### Response Example[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id104)

```
{
    "volume": {
        "status": "available",
        "attachments": [],
        "links": [
            {
                "href": "http://localhost:8776/v3/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                "rel": "self"
            },
            {
                "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                "rel": "bookmark"
            }
        ],
        "availability_zone": "nova",
        "bootable": "false",
        "os-vol-host-attr:host": "ip-10-168-107-25",
        "source_volid": null,
        "snapshot_id": null,
        "id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
        "description": "Super volume.",
        "name": "vol-002",
        "created_at": "2013-02-25T02:40:21.000000",
        "volume_type": null,
        "os-vol-tenant-attr:tenant_id": "0c2eba2c5af04d3f9e9d0d410b371fde",
        "size": 1,
        "metadata": {
            "contents": "not junk"
        }
    }
}
```

### Delete a volume	DELETE		/v3/{project_id}/volumes/{volume_id}

Preconditions

- Volume status must be `available`, `in-use`, `error`, `error_restoring`, `error_extending`, `error_managing`, and must not be migrating, attached, belong to a group or have snapshots.
- You cannot already have a snapshot of the volume.
- You cannot delete a volume that is in a migration.

Asynchronous Postconditions

- The volume is deleted in volume index.
- The volume managed by OpenStack Block Storage is deleted in storage node.

Troubleshooting

- If volume status remains in `deleting` or becomes `error_deleting` the request failed. Ensure you meet the preconditions then investigate the storage back end.
- The volume managed by OpenStack Block Storage is not deleted from the storage system.

#### Response codes[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id112)

##### Success[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#Success)

| Code             | Reason                                                  |
| ---------------- | ------------------------------------------------------- |
| `202 - Accepted` | Request is accepted, but processing may take some time. |

#### Request[¶](https://developer.openstack.org/api-ref/block-storage/v3/index.html?expanded=delete-a-volume-detail,show-a-volume-s-details-detail,list-accessible-volumes-detail,create-a-volume-detail,list-accessible-volumes-with-details-detail#id113)

| Name               | In   | Type    | Description                                                  |
| ------------------ | ---- | ------- | ------------------------------------------------------------ |
| project_id         | path | string  | The UUID of the project in a multi-tenancy cloud.            |
| volume_id          | path | string  | The UUID of the volume.                                      |
| cascade (Optional) | path | boolean | Remove any snapshots along with the volume. Default=False.   |
| force (Optional)   | path | boolean | Indicates whether to force delete a volume even if the volume is in deleting or error_deleting. Default is `false`.**New in version 3.23** |