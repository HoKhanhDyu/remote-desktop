current_time = time()

        if self.last_frame_time is not None:
            time_diff = current_time - self.last_frame_time
            fps = 1 / time_diff if time_diff > 0 else 0
            print(f"FPS: {fps}")

        self.last_frame_time = current_time