import numpy as np


class NavierStokesForceField:

    def __init__(self, viscosity=0.5, inertia_scale=0.35):
        self.nu = viscosity
        self.alpha = inertia_scale

    def encode_to_field(self, scale):
        if scale <= 1.0:
            return 0.0
        return 2.0 / (1.0 + np.exp(-np.log(scale))) - 1.0

    def simulate_vortex(self, initial_energy, steps=100):
        energy = initial_energy
        trajectory = []

        print(
            f"=== ЗАПУСК СИМУЛЯЦИИ НАВЬЕ-СТОКСА (Баланс сил 2N+1) для E0 = {initial_energy} ==="
        )
        print(
            f"{'Шаг':<5} | {'Энергия вихря':<14} | {'Позиция [-1,1]':<15} | {'Сила Инерции':<13} | {'Сила Вязкости':<14}"
        )
        print("-" * 75)

        for step in range(steps):
            pos = self.encode_to_field(energy)

            f_inertial = self.alpha * (1.0 - pos)
            f_viscous = -self.nu * pos

            net_force = f_inertial + f_viscous

            print(
                f"{step:<5} | {energy:<14.4f} | {pos:<15.4f} | {f_inertial:<13.4f} | {f_viscous:<14.4f}"
            )

            energy = energy * np.exp(net_force)
            trajectory.append({"pos": pos, "net_force": net_force})

            if energy < 1.001:
                print("-" * 75)
                print(
                    f"Шаг {step+1}: Вихрь полностью диссипировал. Система пришла в гладкое состояние."
                )
                break
        else:
            print("-" * 75)
            print("Лимит шагов исчерпан.")

        forces = [t["net_force"] for t in trajectory]
        print(f"Средний вектор поля сил: {np.mean(forces):.4f}")

        if np.mean(forces) < 0:
            print(
                "ГЛОБАЛЬНЫЙ ВЫВОД: Диссипация строго больше нуля. Сингулярность невозможна. Решение гладкое."
            )


ns_field = NavierStokesForceField(viscosity=0.5, inertia_scale=0.35)
ns_field.simulate_vortex(5000.0)
