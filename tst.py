    def generate_food(self):
        while True:
            food = (
                random.randint(
                    0, (self.width - self.cell_size) // self.cell_size
                )
                * self.cell_size,
                random.randint(0, (self.height - self.cell_size) //
                self.cell_size)
                * self.cell_size
            )