from sim.blinking_vortex_sim import BlinkingVortexSim
import argparse


def run_simulation(num_particles, mu, duration, output_video, show_plot, fps):
    sim = BlinkingVortexSim(mu, num_particles)
    sim.simulate(duration, fps, save_state=True, status_bar=True)
    if output_video is not None:
        sim.generate_video(output_video, fps)
    if show_plot:
        sim.plot_mixing()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A simulation of the Aref blinking vortex flow")
    parser.add_argument('-n', dest='n', type=int, default=100000,
                        help='The number of particles to simulate. Output density resolution'
                             'will improve with larger numbers')
    parser.add_argument('--mu', dest='mu', type=float, default=1.0,
                        help='The simulation parameter. See documentation for description')
    parser.add_argument('--output', type=str, dest='output',
                        help='The output file for the simulation video. If none is specified, '
                             'no video will be generated.')
    parser.add_argument('--fps', type=int, dest='fps', default=10,
                        help='The FPS of the generated video. Higher FPS will take longer to simulate')
    parser.add_argument('--plot', dest='plot', action='store_true', default=False,
                        help='Whether to show the mixing rate plot.')
    parser.add_argument('--duration', type=int, default=5, dest='duration',
                        help='The number of cycles to run the simulation.')

    args = parser.parse_args()
    run_simulation(args.n, args.mu, args.duration, args.output, args.plot, args.fps)
