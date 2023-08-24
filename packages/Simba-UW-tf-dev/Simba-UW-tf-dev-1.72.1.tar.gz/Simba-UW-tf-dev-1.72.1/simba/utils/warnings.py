__author__ = "Simon Nilsson"

import logging
from simba.utils.printing import stdout_warning

def ThirdPartyAnnotationsOutsidePoseEstimationDataWarning(video_name: str,
                                                          frm_cnt: int,
                                                          log_status: bool = False,
                                                          clf_name: str or None = None,
                                                          annotation_frms: int or None = None,
                                                          first_error_frm: int or None=None,
                                                          ambiguous_cnt: int or None=None,
                                                          ):
    if clf_name:
        msg = (f'SIMBA THIRD-PARTY ANNOTATION WARNING: SimBA found THIRD-PARTY annotations for behavior {clf_name} in video '
               f'{video_name} that are annotated to occur at times which is not present in the '
               f'video data you imported into SIMBA. The video you imported to SimBA has {str(frm_cnt)} frames. '
               f'However, in BORIS, you have annotated {clf_name} to happen at frame number {str(first_error_frm)}. '
               f'These ambiguous annotations occur in {str(ambiguous_cnt)} different frames for video {video_name} that SimBA will **remove** by default. '
               f'Please make sure you imported the same video as you annotated in BORIS into SimBA and the video is registered with the correct frame rate. '
               f'SimBA will only append annotations made to the frames present in the pose estimation data.')
    else:
        msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: The annotations for video {video_name} contain data for {str(annotation_frms)} frames. The pose-estimation features for the same video contain data for {str(frm_cnt)} frames. SimBA will use the annotations for the frames present in the pose-estimation data and discard the rest. If the annotation data is shorter than the pose-estimation data, SimBA will assume the missing annotation frames are all behavior absent.'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def ThirdPartyAnnotationsClfMissingWarning(video_name: str,
                                              clf_name: str):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: No annotations detected for video {video_name} and behavior {clf_name}. ' \
          f'SimBA will set all frame annotations as absent.'
    stdout_warning(msg=msg)

def ThirdPartyAnnotationsAdditionalClfWarning(video_name: str,
                                              clf_names: list,
                                              log_status: bool=False):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: Annotations file for video {video_name} has annotations for the following behaviors {clf_names} that are NOT classifiers named in the SimBA project. SimBA will OMIT appending the data for these {str(len(clf_names))} classifiers.'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)


def ThirdPartyAnnotationsInvalidFileFormatWarning(annotation_app: str,
                                                  file_path: str,
                                                  log_status: bool=False):
    msg = f'SIMBA WARNING: {file_path} is not a valid {annotation_app} file and is skipped. See the SimBA GitHub repository for expected file format'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def ThirdPartyAnnotationsMissingAnnotationsWarning(video_name: str,
                                                   clf_names: list,
                                                   log_status: bool=False):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: No annotations detected for SimBA classifier(s) named {clf_names} for video {video_name}. All frame annotations will be set to behavior absent (0).'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def ThirdPartyAnnotationsFpsConflictWarning(video_name: str,
                                            annotation_fps: int,
                                            video_fps: int):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: The FPS for video {video_name} is set to {str(video_fps)} in SimBA and {str(annotation_fps)} in the annotation file'
    stdout_warning(msg=msg)


def ThirdPartyAnnotationEventCountWarning(video_name: str, clf_name: str, start_event_cnt: int, stop_event_cnt: int, log_status: bool=False):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: The annotations for behavior {clf_name} in video {video_name} contains {str(start_event_cnt)} start events and {str(stop_event_cnt)} stop events. SimBA requires the number of stop and start event counts to be equal. SimBA will try to find and delete the odd event stamps.'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def ThirdPartyAnnotationOverlapWarning(video_name: str,
                                       clf_name: str,
                                       log_status: bool=False):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: The annotations for behavior {clf_name} in video {video_name} contains behavior start events that are initiated PRIOR to the PRECEDING behavior event ending. SimBA requires a specific behavior event to end before another behavior event can start. SimBA will try and delete these events.'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def ThirdPartyAnnotationFileNotFoundWarning(video_name: str, log_status: bool=False):
    msg = f'SIMBA THIRD-PARTY ANNOTATION WARNING: Could not find annotations for video features file {video_name} in the annotations directory.'
    if log_status: logging.warning(msg=msg)
    stdout_warning(msg=msg)

def BodypartColumnNotFoundWarning(msg: str):
    stdout_warning(msg=f'SIMBA BODY-PART COLUMN NOT FOUND WARNING: {msg}')

def ShapWarning(msg: str):
    stdout_warning(msg=f'SIMBA SHAP WARNING: {msg}')

def InValidUserInputWarning(msg: str):
    stdout_warning(msg=f'SIMBA USER INPUT WARNING: {msg}')

def KleinbergWarning(msg: str):
    stdout_warning(msg=f'SIMBA KLEINBERG WARNING: {msg}')

def NoFileFoundWarning(msg: str):
    stdout_warning(msg=f'SIMBA NO FILE FOUND WARNING: {msg}')

def DataHeaderWarning(msg: str):
    stdout_warning(msg=f'SIMBA DATA HEADER WARNING: {msg}')

def NoModuleWarning(msg: str):
    stdout_warning(msg=f'SIMBA NO MODULE WARNING: {msg}')

def FileExistWarning(msg: str):
    stdout_warning(msg=f'SIMBA FILE EXIST WARNING: {msg}')

def DuplicateNamesWarning(msg: str):
    stdout_warning(msg=f'SIMBA DUPLICATE NAMES WARNING: {msg}')

def InvalidValueWarning(msg: str):
    stdout_warning(msg=f'SIMBA INVALID VALUE WARNING: {msg}')

def NoDataFoundWarning(msg: str):
    stdout_warning(msg=f'SIMBA NO DATA FOUND WARNING: {msg}')

def NotEnoughDataWarning(msg: str):
    stdout_warning(msg=f'SIMBA NOT ENOUGH DATA WARNING: {msg}')

def MissingUserInputWarning(msg: str):
    stdout_warning(msg=f'SIMBA MISSING USER SPECIFICATION WARNING: {msg}')

def SameInputAndOutputWarning(msg: str):
    stdout_warning(msg=f'SIMBA INPUT AND OUTPUT WARNING: {msg}')

def ROIWarning(msg: str):
    stdout_warning(msg=f'SIMBA ROI WARNING: {msg}')

def MultiProcessingFailedWarning(msg: str):
    stdout_warning(msg=f'SIMBA MULTI-PROCESSING WARNING: {msg}')

def PythonVersionWarning(msg: str):
    stdout_warning(msg=f'SIMBA PYTHON VERSION WARNING: {msg}')

def BorisPointEventsWarning(msg: str):
    stdout_warning(msg=f'SIMBA BORIS POINT EVENT WARNING: {msg}')

def FFMpegCodecWarning(msg: str):
    stdout_warning(msg=f'SIMBA FFMPEG CODEC WARNING: {msg}')

def FFMpegNotFoundWarning(msg: str):
    stdout_warning(msg=f'SIMBA FFMPEG NOT FOUND WARNING: {msg}')

def SkippingFileWarning(msg: str):
    stdout_warning(msg=f'SIMBA SKIPPING FILE WARNING: {msg}')

def SkippingRuleWarning(msg: str):
    stdout_warning(msg=f'SIMBA SKIPPING RULE WARNING: {msg}')

def IdenticalInputWarning(msg: str):
    stdout_warning(msg=f'SIMBA IDENTICAL WARNING: {msg}')