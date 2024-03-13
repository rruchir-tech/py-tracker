#!/usr/bin/python3

from gps_sms_call_button import GpsSMSCall


config = {
    'phone_number': '5102988763',
    'sms_prefix_msg': 'I am at this location',
    'call_duration': 20,
    'kml_file_path': '/home/avengers/py-tracker/kml_files/Home_Fence.kml'
    #'kml_file_path': '/home/avengers/py-tracker/kml_files/School_Fence.kml',
    #'kml_file_path': '/home/avengers/py-tracker/kml_files/Chabot college fence.kml'
}

gpsSmsCall = GpsSMSCall()
gpsSmsCall.setup()
gpsSmsCall.check_inside_fence(config)

gpsSmsCall.shutdown()
