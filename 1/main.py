from video import capture_from_camera, capture_from_file


def main(filepath=None):
    if filepath is None:
        capture_from_camera()
    else:
        capture_from_file(filepath)


if __name__ == '__main__':
    main('../resources/video.mp4')
