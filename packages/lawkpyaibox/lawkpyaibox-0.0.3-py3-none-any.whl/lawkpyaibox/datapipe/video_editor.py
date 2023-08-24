from distutils.log import error
import cv2
import numpy as np
import time
from .datathread import thread_show_progress


def merge_videos_with_startidx(videopath_lst,
                               outputpath,
                               merged_startidx=0,
                               axis=0):
    print("\nStart merge_videos_with_startidx")
    videoattrlst = {
        "videocap": [],
        "imgnums": [],
        "fps": [],
        "width": [],
        "height": []
    }

    for vididx, videopath in enumerate(videopath_lst):
        cap = cv2.VideoCapture(videopath)
        imgnums = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, merged_startidx)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        videoattrlst["videocap"].append(cap)
        videoattrlst["imgnums"].append(imgnums)
        videoattrlst["fps"].append(fps)
        videoattrlst["width"].append(width)
        videoattrlst["height"].append(height)
    assert len(set(videoattrlst["fps"])), "input videos fps must be same"
    imgnum = min(videoattrlst["imgnums"])

    if axis == 0:
        assert len(set(videoattrlst["height"])
                   ), "input-videos height must be same when axis=0"
        size = (int(sum(videoattrlst["width"])),
                int(videoattrlst["height"][0]))
    else:
        assert len(set(videoattrlst["width"])
                   ), "input-videos width must be same when axis=0"
        size = (int(videoattrlst["width"][0]),
                int(sum(videoattrlst["height"])))

    st = time.time()
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video_writer = cv2.VideoWriter(outputpath, fourcc, videoattrlst["fps"][0],
                                   size)
    for imgidx in range(merged_startidx, imgnum):
        imglst = []
        for vididx, cap in enumerate(videoattrlst["videocap"]):
            ret, img = cap.read()
            imglst.append(img)
        if axis == 0:
            mergeimg = np.hstack(imglst)
        else:
            mergeimg = np.vstack(imglst)
        cv2.putText(mergeimg, 'idx: {}'.format(imgidx), (50, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        video_writer.write(mergeimg)
        et = time.time()
        if imgidx % 200 == 0:
            thread_show_progress(0, et, st, imgidx, imgnum,
                                 "videos are merging, ")

    for vididx, cap in enumerate(videoattrlst["videocap"]):
        cap.release()
    video_writer.release()
    print("Merge videos done!\n")
