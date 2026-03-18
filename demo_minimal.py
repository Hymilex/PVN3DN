#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Minimal PVN3D forward demo")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument(
        "--num-points",
        type=int,
        default=4096,
        help="Must be >= 2048 for the default PointNet++ sampling layers.",
    )
    parser.add_argument("--num-classes", type=int, default=22)
    parser.add_argument("--height", type=int, default=128)
    parser.add_argument("--width", type=int, default=128)
    parser.add_argument("--cpu", action="store_true", help="Force CPU execution.")
    return parser.parse_args()


def main():
    args = parse_args()

    repo_root = Path(__file__).resolve().parent
    package_root = repo_root / "pvn3d"
    if str(package_root) not in sys.path:
        sys.path.insert(0, str(package_root))

    try:
        import torch
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "PyTorch is not installed in the current environment. "
            "Install torch first, then rerun demo_minimal.py."
        ) from exc

    from pvn3d.lib.pvn3d import PVN3D

    if args.num_points < 2048:
        raise ValueError("--num-points must be >= 2048")

    device = torch.device(
        "cpu" if args.cpu or not torch.cuda.is_available() else "cuda"
    )

    bs = args.batch_size
    num_points = args.num_points
    num_classes = args.num_classes
    height = args.height
    width = args.width

    # PVN3D expects point features as xyz + rgb + normal => 9 dims total.
    pointcloud = torch.randn(bs, num_points, 9, device=device)
    rgb = torch.randn(bs, 3, height, width, device=device)
    choose = torch.randint(0, height * width, (bs, 1, num_points), device=device)

    model = PVN3D(
        num_classes=num_classes,
        pcld_input_channels=6,
        pcld_use_xyz=True,
        num_points=num_points,
    ).to(device)
    model.eval()

    with torch.no_grad():
        pred_kp_of, pred_rgbd_seg, pred_ctr_of = model(pointcloud, rgb, choose)

    print("Device:", device)
    print("Keypoint offset pred shape:", tuple(pred_kp_of.shape))
    print("Segmentation pred shape:", tuple(pred_rgbd_seg.shape))
    print("Center offset pred shape:", tuple(pred_ctr_of.shape))
    print("Demo run success!")


if __name__ == "__main__":
    main()
