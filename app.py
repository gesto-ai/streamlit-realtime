import av
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer


def app():
    class VideoProcessor(VideoProcessorBase):
        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            flipped = img[:,::-1,:] 

            return av.VideoFrame.from_ndarray(flipped, format="bgr24")

    def out_recorder_factory() -> MediaRecorder:
        return MediaRecorder("user_recording.mp4", format="mp4")

    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={
            "video": True,
            "audio": False,
        },
        video_processor_factory=VideoProcessor,
        out_recorder_factory=out_recorder_factory,
    )


if __name__ == "__main__":
    app()