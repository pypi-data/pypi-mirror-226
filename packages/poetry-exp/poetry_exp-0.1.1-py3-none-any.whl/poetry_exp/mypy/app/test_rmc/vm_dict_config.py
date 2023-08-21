vm_conf_dict = {'swapStorageObjectId': None, 'changeVersion': '', 'datastoreUrl':  [
    {
      "dynamicType": None,
      "dynamicProperty":  [],
      "name": 'Nimble_VVOL',
      "url": '/vmfs/volumes/vvol:0000000d00004000-85a53827ddda510d/'
   }
], 'dynamicProperty':  [], 'cpuAffinity': None, 'messageBusTunnelEnabled': False, 'cpuHotRemoveEnabled': False, 'vFlashCacheReservation': 0, 'networkShaper': None, 'memoryReservationLockedToMax': False, 'vmxConfigChecksum': None, 'hardware':  {
   "dynamicType": None,
   "dynamicProperty": [],
   "numCPU ": 2,
   "numCoresPerSocket ": 2,
   "memoryMB ": 4096,
   "virtualICH7MPresent ": False,
   "virtualSMCPresent ": False,
   "device ":  [
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 200,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'IDE 0',
            "summary ": 'IDE 0'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": None,
         "unitNumber ": None,
         "busNumber ": 0,
         "device ":  [
            3000
         ]
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 201,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'IDE 1',
            "summary ": 'IDE 1'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": None,
         "unitNumber ": None,
         "busNumber ": 1,
         "device ":  []
      },
      {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 300,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'PS2 controller 0',
            "summary ": 'PS2 controller 0'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": None,
         "unitNumber ": None,
         "busNumber ": 0,
         "device ":  [
            600,
            700
         ]
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 100,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'PCI controller 0',
            "summary ": 'PCI controller 0'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller ": None,
         "unitNumber ": None,
         "busNumber ": 0,
         "device ":  [
            500,
            12000,
            1000,
            4000
         ]
      },
      {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 400,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'SIO controller 0',
            "summary ": 'SIO controller 0'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": None,
         "unitNumber ": None,
         "busNumber ": 0,
         "device ":  []
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 600,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'Keyboard ',
            "summary ": 'Keyboard'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": 300,
         "unitNumber ": 0
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 700,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'Pointing device',
            "summary ": 'Pointing device; Device'
         },
         "backing ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "deviceName ": '',
            "useAutoDetect ": False,
            "device ": 'autodetect'
         },
         "connectable ": None,
         "slotInfo ": None,
         "controller": 300,
         "unitNumber ": 1
      },
      {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 500,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'Video card ',
            "summary ": 'Video card'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": 100,
         "unitNumber ": 0,
         "videoRamSizeInKB ": 8192,
         "numDisplays ": 1,
         "useAutoDetect ": False,
         "enable3DSupport ": False,
         "use3dRenderer ": 'automatic',
         "graphicsMemorySizeInKB ": 262144
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 12000,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'VMCI device',
            "summary ": 'Device on the virtual machine PCI bus that provides support for the virtual machine communication interface'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": 100,
         "unitNumber ": 17,
         "id ": -1,
         "allowUnrestrictedCommunication ": False,
         "filterEnable ": True,
         "filterInfo ": None
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 1000,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'SCSI controller 0',
            "summary ": 'LSI Logic SAS'
         },
         "backing ": None,
         "connectable ": None,
         "slotInfo ": None,
         "controller": 100,
         "unitNumber ": 3,
         "busNumber ": 0,
         "device ":  [
            2000
         ],
         "hotAddRemove ": True,
         "sharedBus ": 'noSharing',
         "unitNumber ": 7
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 3000,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'CD/DVD drive 1',
            "summary ": 'Remote device'
         },
         "backing ": {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "deviceName ": '',
            "useAutoDetect ": False,
            "exclusive ": False
         },
         "connectable ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "startconnected ": False,
            "allowGuestControl ": True,
            "connected ": False,
            "status ": 'untried'
         },
         "slotInfo ": None,
         "controller": 200,
         "unitNumber ": 0
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 2000,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'Hard disk 1',
            "summary ": '2,097,152 KB'
         },
         "backing ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000013.vmdk',
            "datastore ": 'vim.Datastore:datastore-7284',
            "backingObjectId ": 'rfc4122.ba13db75-4a08-4e4f-912c-8f070a3a36c5',
            "diskMode ": 'persistent',
            "split ": False,
            "writeThrough ": False,
            "thinProvisioned ": True,
            "eagerlyScrub ": None,
            "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
            "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
            "changeId ": None,
            "parent ":  {
               "dynamicType ": None,
               "dynamicProperty ":  [],
               "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000012.vmdk',
               "datastore ": 'vim.Datastore:datastore-7284',
               "backingObjectId ": 'rfc4122.2909f833-2e19-487f-b2a4-e827d52b9d53',
               "diskMode ": 'persistent',
               "split ": None,
               "writeThrough ": None,
               "thinProvisioned ": True,
               "eagerlyScrub ": None,
               "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
               "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
               "changeId ": None,
               "parent ":  {
                  "dynamicType ": None,
                  "dynamicProperty ":  [],
                  "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000011.vmdk',
                  "datastore ": 'vim.Datastore:datastore-7284',
                  "backingObjectId ": 'rfc4122.2e41a01d-9703-44c1-8bc7-e3f1fcbe6ee0',
                  "diskMode ": 'persistent',
                  "split ": None,
                  "writeThrough ": None,
                  "thinProvisioned ": True,
                  "eagerlyScrub ": None,
                  "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                  "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                  "changeId ": None,
                  "parent ":  {
                     "dynamicType ": None,
                     "dynamicProperty ":  [],
                     "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000010.vmdk',
                     "datastore ": 'vim.Datastore:datastore-7284',
                     "backingObjectId ": 'rfc4122.f3be3302-3f57-450e-930f-78241af9006d',
                     "diskMode ": 'persistent',
                    "split ": None,
                     "writeThrough ": None,
                     "thinProvisioned ": True,
                     "eagerlyScrub ": None,
                     "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                     "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                     "changeId ": None,
                     "parent ":  {
                        "dynamicType ": None,
                        "dynamicProperty ":  [],
                        "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000005.vmdk',
                        "datastore ": 'vim.Datastore:datastore-7284',
                        "backingObjectId ": 'rfc4122.f21d8af5-7e7d-4f91-9c99-8d8bcdb35a16',
                        "diskMode ": 'persistent',
                       "split ": None,
                        "writeThrough ": None,
                        "thinProvisioned ": True,
                        "eagerlyScrub ": None,
                        "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                        "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                        "changeId ": None,
                        "parent ":  {
                           "dynamicType ": None,
                           "dynamicProperty ":  [],
                           "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000009.vmdk',
                           "datastore ": 'vim.Datastore:datastore-7284',
                           "backingObjectId ": 'rfc4122.0ad747c4-4691-4f29-8b0d-683815b7008a',
                           "diskMode ": 'persistent',
                          "split ": None,
                           "writeThrough ": None,
                           "thinProvisioned ": True,
                           "eagerlyScrub ": None,
                           "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                           "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                           "changeId ": None,
                           "parent ":  {
                              "dynamicType ": None,
                              "dynamicProperty ":  [],
                              "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000008.vmdk',
                              "datastore ": 'vim.Datastore:datastore-7284',
                              "backingObjectId ": 'rfc4122.23d976b9-7915-41e5-8529-76e963a53665',
                              "diskMode ": 'persistent',
                             "split ": None,
                              "writeThrough ": None,
                              "thinProvisioned ": True,
                              "eagerlyScrub ": None,
                              "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                              "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                              "changeId ": None,
                              "parent ":  {
                                 "dynamicType ": None,
                                 "dynamicProperty ":  [],
                                 "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000007.vmdk',
                                 "datastore ": 'vim.Datastore:datastore-7284',
                                 "backingObjectId ": 'rfc4122.7b8d86b0-0f27-4c47-b7a8-e310980b08f8',
                                 "diskMode ": 'persistent',
                                "split ": None,
                                 "writeThrough ": None,
                                 "thinProvisioned ": True,
                                 "eagerlyScrub ": None,
                                 "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                                 "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                                 "changeId ": None,
                                 "parent ":  {
                                    "dynamicType ": None,
                                    "dynamicProperty ":  [],
                                    "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000006.vmdk',
                                    "datastore ": 'vim.Datastore:datastore-7284',
                                    "backingObjectId ": 'rfc4122.d1479bff-680c-4ee3-a5fd-c34bbc3c726e',
                                    "diskMode ": 'persistent',
                                   "split ": None,
                                    "writeThrough ": None,
                                    "thinProvisioned ": True,
                                    "eagerlyScrub ": None,
                                    "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                                    "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                                    "changeId ": None,
                                    "parent ":  {
                                       "dynamicType ": None,
                                       "dynamicProperty ":  [],
                                       "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000002.vmdk',
                                       "datastore ": 'vim.Datastore:datastore-7284',
                                       "backingObjectId ": 'rfc4122.22019129-d231-4157-909d-c149d85e436a',
                                       "diskMode ": 'persistent',
                                      "split ": None,
                                       "writeThrough ": None,
                                       "thinProvisioned ": True,
                                       "eagerlyScrub ": None,
                                       "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                                       "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                                       "changeId ": None,
                                       "parent ":  {
                                          "dynamicType ": None,
                                          "dynamicProperty ":  [],
                                          "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1-000001.vmdk',
                                          "datastore ": 'vim.Datastore:datastore-7284',
                                          "backingObjectId ": 'rfc4122.83e2dd1e-c29b-435e-b0f3-dd0597cc9cf9',
                                          "diskMode ": 'persistent',
                                         "split ": None,
                                          "writeThrough ": None,
                                          "thinProvisioned ": True,
                                          "eagerlyScrub ": None,
                                          "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                                          "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                                          "changeId ": None,
                                          "parent ":  {
                                             "dynamicType ": None,
                                             "dynamicProperty ":  [],
                                             "fileName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1.vmdk',
                                             "datastore ": 'vim.Datastore:datastore-7284',
                                             "backingObjectId ": 'rfc4122.2b7d9df3-e668-47b6-964b-7fdad2da737b',
                                             "diskMode ": 'persistent',
                                            "split ": None,
                                             "writeThrough ": None,
                                             "thinProvisioned ": True,
                                             "eagerlyScrub ": None,
                                             "uuid ": '6000C29d-1650-b2a0-8261-3e8c9a422c6c',
                                             "contentId ": 'a1cf528f9b287bf902f29c42fffffffe',
                                             "changeId ": None,
                                             "parent ": None,
                                             "deltaDiskFormat ": None,
                                             "digestEnabled ": False,
                                             "deltaGrainSize ": None,
                                             "deltaDiskFormatVariant ": None,
                                             "sharing ": None
                                          },
                                          "deltaDiskFormat ": 'nativeFormat',
                                          "digestEnabled ": False,
                                          "deltaGrainSize ": None,
                                          "deltaDiskFormatVariant ": None,
                                          "sharing ": None
                                       },
                                       "deltaDiskFormat ": 'nativeFormat',
                                       "digestEnabled ": False,
                                       "deltaGrainSize ": None,
                                       "deltaDiskFormatVariant ": None,
                                       "sharing ": None
                                    },
                                    "deltaDiskFormat ": 'nativeFormat',
                                    "digestEnabled ": False,
                                    "deltaGrainSize ": None,
                                    "deltaDiskFormatVariant ": None,
                                    "sharing ": None
                                 },
                                 "deltaDiskFormat ": 'nativeFormat',
                                 "digestEnabled ": False,
                                 "deltaGrainSize ": None,
                                 "deltaDiskFormatVariant ": None,
                                 "sharing ": None
                              },
                              "deltaDiskFormat ": 'nativeFormat',
                              "digestEnabled ": False,
                              "deltaGrainSize ": None,
                              "deltaDiskFormatVariant ": None,
                              "sharing ": None
                           },
                           "deltaDiskFormat ": 'nativeFormat',
                           "digestEnabled ": False,
                           "deltaGrainSize ": None,
                           "deltaDiskFormatVariant ": None,
                           "sharing ": None
                        },
                        "deltaDiskFormat ": 'nativeFormat',
                        "digestEnabled ": False,
                        "deltaGrainSize ": None,
                        "deltaDiskFormatVariant ": None,
                        "sharing ": None
                     },
                     "deltaDiskFormat ": 'nativeFormat',
                     "digestEnabled ": False,
                     "deltaGrainSize ": None,
                     "deltaDiskFormatVariant ": None,
                     "sharing ": None
                  },
                  "deltaDiskFormat ": 'nativeFormat',
                  "digestEnabled ": False,
                  "deltaGrainSize ": None,
                  "deltaDiskFormatVariant ": None,
                  "sharing ": None
               },
               "deltaDiskFormat ": 'nativeFormat',
               "digestEnabled ": False,
               "deltaGrainSize ": None,
               "deltaDiskFormatVariant ": None,
               "sharing ": None
            },
            "deltaDiskFormat ": 'nativeFormat',
            "digestEnabled ": False,
            "deltaGrainSize ": None,
            "deltaDiskFormatVariant ": None,
            "sharing ": 'sharingNone'
         },
         "connectable ": None,
         "slotInfo ": None,
         "controller": 1000,
         "unitNumber ": 0,
         "capacityInKB ": 2097152,
         "capacityInBytes ": 2147483648,
         "shares ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "shares ": 1000,
            "level ": 'normal'
         },
         "storageIOAllocation ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "limit ": -1,
            "shares ":  {
               "dynamicType ": None,
               "dynamicProperty ":  [],
               "shares ": 1000,
               "level ": 'normal'
            },
            "reservation ": 0
         },
         "diskObjectId ": '187-2000',
         "vFlashCacheConfigInfo ": None,
         "iofilter ": []
      },
       {
         "dynamicType ": None,
         "dynamicProperty ":  [],
         "key ": 4000,
         "deviceInfo ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "label ": 'Network adapter 1',
            "summary ": 'VM Network'
         },
         "backing ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "deviceName ": 'VM Network',
            "useAutoDetect ": False,
            "network ": 'vim.Network:network-11',
            "inPassthroughMode ": None
         },
         "connectable ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "startconnected ": True,
            "allowGuestControl ": True,
            "connected ": False,
            "status ": 'untried'
         },
         "slotInfo ": None,
         "controller": 100,
         "unitNumber ": 7,
         "addressType ": 'assigned',
         "macAddress ": '00:50:56:9d:d6:ce',
         "wakeOnLanEnabled ": True,
         "resourceAllocation ":  {
            "dynamicType ": None,
            "dynamicProperty ":  [],
            "reservation ": 0,
            "share ":  {
               "dynamicType ": None,
               "dynamicProperty ":  [],
               "shares ": 50,
               "level ": 'normal'
            },
            "limit ": -1
         },
         "externalId ": None,
         "uptCompatibilityEnabled ": False
      }
   ]
}, 'consolePreferences': None, 'npivTemporaryDisabled': True, 'vmStorageObjectId': None, 'scheduledHardwareUpgradeInfo':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "upgradePolicy ": 'never',
   "version ": None,
   "scheduledHardwareUpgrade": 'none',
   "fault ": None
}, 'firmware': 'bios', 'guestAutoLockEnabled': False, 'tools':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "toolsVersion ": 0,
   "afterPowerOn ": True,
   "afterResume ": True,
   "beforeGuestStandby ": True,
   "beforeGuestShutdown ": True,
   "beforeGuestReboot ": None,
   "toolsUpgradePolicy ": 'manual',
   "pendingCustomization ": None,
   "syncTimeWithHost ": False,
   "lastInstallInfo ": None
}, 'guestFullName': 'Microsoft Windows Server 2012 (64-bit)', 'npivDesiredPortWwns': None, 'vAppConfig': None, 'instanceUuid': '501d6576-d3cc-ce89-4f92-69c91c48ae3f', 'uuid': '421dbb7e-8b57-0703-bfca-6979ce47321c', 'forkConfigInfo': None, 'repConfig': None, 'npivOnNonRdmDisks': None, 'memoryHotAddEnabled': False, 'cpuAllocation':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "reservation ": 0,
   "expandablereservation ": False,
   "limit ": -1,
   "shares ":  {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "shares ": 2000,
      "level ": 'normal'
   },
   "overhead": None
}, 'version': 'vmx-14', 'template': False, 'memoryAllocation':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "reservation ": 0,
   "expandableReservation ": False,
   "limit ": -1,
   "shares ":  {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "shares ": 40960,
      "level ": 'normal'
   },
   "overheadlimit ": None
}, 'ftInfo': None, 'cpuHotAddEnabled': False, 'npivNodeWorldWideName':  [], 'hotPlugMemoryLimit': None, 'files':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "vmPathName ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/VVOL1_VM1.vmx',
   "snapshotDirectory ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/',
   "suspendDirectory ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/',
   "logDirectory ": '[Nimble_VVOL] rfc4122.ef0589db-0de2-4a97-865e-ac9a8fb0d57a/',
   "ftMetadataDirectory ": None
}, 'alternateGuestName': '', 'extraConfig':  [
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'nvram',
      "value ": 'VVOL1_VM1.nvram'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge0.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'svga.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge4.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge4.virtualDev',
      "value ": 'pcieRootPort'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge4.functions',
      "value ": '8'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge5.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge5.virtualDev',
      "value ": 'pcieRootPort'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge5.functions',
      "value ": '8'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge6.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge6.virtualDev',
      "value ": 'pcieRootPort'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge6.functions',
      "value ": '8'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge7.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge7.virtualDev',
      "value ": 'pcieRootPort'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'pciBridge7.functions',
      "value ": '8'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'hpet0.present',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'cpuid.coresPerSocket',
      "value ": '2'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'sched.cpu.latencySensitivity',
      "value ": 'normal'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'disk.EnableUUID',
      "value ": 'True'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'migrate.hostLog',
      "value ": 'VVOL1_VM1-3870c78e.hlog'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'vmware.tools.internalversion',
      "value ": '0'
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "key ": 'vmware.tools.requiredversion',
      "value ": '10341'
   }
], 'nestedHVEnabled': False, 'swapPlacement': 'inherit', 'locationId': '', 'guestId': 'windows8Server64Guest', 'bootOptions': {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "bootDelay ": 0,
   "enterBIOSSetup ": False,
   "bootRetryEnabled ": False,
   "bootRetryDelay ": 10000,
   "bootOrder ": [],
   "networkBootProtocol ": 'ipv4'
}, 'npivPortWorldWideName':  [], 'annotation': '', 'defaultPowerOps':  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "powerOffType ": 'soft',
   "suspendType ": 'hard',
   "resetType ": 'soft',
   "defaultPowerOffType ": 'soft',
   "defaultSuspendType ": 'hard',
   "defaultResetType ": 'soft',
   "standbyAction ": 'checkpoint'
}, 'vAssertsEnabled': False, 'hotPlugMemoryIncrementSize': None, 'changeTrackingEnabled': False, 'name': 'VVOL1_VM1', 'managedBy': None, 'dynamicType': None, 'npivDesiredNodeWwns': None, 'npivWorldWideNameType': None, 'modified': "datetime.datetime(1970, 1, 1, 0, 0, :<pyVmomi.Iso8601.TZInfo object at 0x7f9588e83cd0>)", "latencySensitivity":  {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "level ": 'normal',
   "sensitivity ": None
},
'flags': {
   "dynamicType ": None,
   "dynamicProperty ":  [],
   "disableAcceleration ": False,
   "enableLogging ": True,
   "useToe ": False,
   "runWithDebugInfo ": False,
   "monitorType ": 'release',
   "sharing ": 'any',
   "snapshotDisabled ": False,
   "snapshotLocked ": False,
   "diskUuidEnabled ": True,
   "virtualMmuUsage ": 'automatic',
   "virtualExecUsage ": 'hvAuto',
   "snapshotPowerOffBehavior ": 'powerOff',
   "recordReplayEnabled ": False,
   "faultToleranceType ": 'unset'
}, 'maxMksConnections': 40, 'cpuFeatureMask':  [
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": 0,
      "vendor ": None,
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": 0,
      "vendor ": 'amd',
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": 1,
      "vendor ": None,
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": 1,
      "vendor ": 'amd',
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483648,
      "vendor ": None,
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483648,
      "vendor ": 'amd',
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483647,
      "vendor ": None,
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483647,
      "vendor ": 'amd',
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483640,
      "vendor ": None,
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   },
    {
      "dynamicType ": None,
      "dynamicProperty ":  [],
      "level ": -2147483640,
      "vendor ": 'amd',
      "eax ": None,
      "ebx ": None,
      "ecx ": None,
      "edx ": None
   }
], 'memoryAffinity': None, 'vPMCEnabled': False, 'initialOverhead': None}