import sys
import pygame
from utils import get_coordinates, find_nearest_pharmacy, calculate_distance, get_map_image


def main():
    if len(sys.argv) != 2:
        print("Использование: python main.py 'адрес'")
        sys.exit(1)

    address = sys.argv[1]

    try:
        origin_coords = get_coordinates(address)
        pharmacy = find_nearest_pharmacy(origin_coords)
        if not pharmacy:
            print("Аптеки не найдены.")
            sys.exit(1)

        distance = calculate_distance(origin_coords[0], origin_coords[1], pharmacy["coords"][0], pharmacy["coords"][1])
        snippet = (
            f"Название: {pharmacy['name']}\n"
            f"Адрес: {pharmacy['address']}\n"
            f"Время работы: {pharmacy['hours']}\n"
            f"Расстояние: {distance:.2f} м"
        )
        print(snippet)
        points = [
            {"lon": origin_coords[0], "lat": origin_coords[1], "icon": "rdm"},  # Исходный адрес
            {"lon": pharmacy["coords"][0], "lat": pharmacy["coords"][1], "icon": "grm"}  # Аптека
        ]

        map_image_data = get_map_image(points)
        with open("map.png", "wb") as file:
            file.write(map_image_data)

        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ближайшая аптека")
        map_image = pygame.image.load("map.png")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            screen.blit(map_image, (0, 0))
            pygame.display.flip()

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
