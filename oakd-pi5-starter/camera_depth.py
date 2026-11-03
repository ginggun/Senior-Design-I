"""Hardware experiment: OAK-D Lite stereo depth on DepthAI v3.

UNVERIFIED ON REAL HARDWARE. Start with the official Luxonis Stereo Depth
example if the installed SDK's API differs. Requires depthai and numpy.
Does NOT implement person recognition or a safe walking system.
"""
from src.obstacle_logic import analyze_depth, describe


def main():
    import depthai as dai

    pipeline = dai.Pipeline()
    left = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    stereo = pipeline.create(dai.node.StereoDepth)
    left.requestFullResolutionOutput().link(stereo.left)
    right.requestFullResolutionOutput().link(stereo.right)
    stereo.setRectification(True)
    stereo.setLeftRightCheck(True)

    # Spatial depth image, not disparity; image frame values are in millimeters.
    queue = stereo.depth.createOutputQueue()
    with pipeline:
        pipeline.start()
        while pipeline.isRunning():
            frame = queue.get()
            # Convert numpy depth frame to rows for the basic algorithm.
            data = frame.getFrame()
            # Subsample to keep Python demonstration lightweight.
            sampled = data[::8, ::8].tolist()
            results = analyze_depth(sampled, min_valid_samples=10)
            print(describe(results), flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nStopped.')
