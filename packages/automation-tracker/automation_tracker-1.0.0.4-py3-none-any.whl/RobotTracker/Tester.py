#import trackerdb and use fucntions from it
from TrackerDB import *

#test the functions in trackerdb
TrackerDB("https://localhost:7063").manually_start_tracker_detailed("POS1",
                                                                                                 "jgitari1",
                                                                                                 "UAT", "CRQ-1234",
                                                                                                 "Q-OPS", "testType",
                                    "API", "200", "100", "50","150","0","0","0","0", "0","0", "0","100","100", "0", "200",
                                                                                                 "TEST-1234")

