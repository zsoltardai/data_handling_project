from data.project.model import DeliveryDataset, DeliveryMethod, FoodType
import numpy as np
import matplotlib.pyplot as plt


def couriers_by_delivery_methods(dataset: DeliveryDataset) -> None:
    properties = ["DeliveryMethod.Car", "DeliveryMethod.Motorcycle", "DeliveryMethod.Bicycle"]

    delivery_methods = [
        DeliveryMethod.Car.name, DeliveryMethod.Motorcycle.name, DeliveryMethod.Bicycle.name
    ]

    values = [
        0, 0, 0
    ]

    for courier in dataset.couriers:
        for delivery_method in delivery_methods:
            if courier.delivery_method == delivery_method:
                values[delivery_methods.index(delivery_method)] += 1

    x = np.arange(len(properties))

    plt.style.use('_mpl-gallery')

    fig, ax = plt.subplots()

    ax.bar(x, values, width=1, edgecolor="white", linewidth=1)
    ax.set_ylabel("Number of couriers")
    ax.set_title("Number of couriers by DeliveryMethods")
    ax.set_xticks(x)
    ax.set_xticklabels(properties)

    fig.tight_layout()

    plt.show()


def clients_by_gender(dataset: DeliveryDataset) -> None:
    properties = ["Person.Male", "Person.Female"]

    values = [
        0, 0
    ]

    for person in dataset.people:
        if person.male:
            values[0] += 1
        else:
            values[1] += 1

    x = np.arange(len(properties))

    plt.style.use('_mpl-gallery')

    fig, ax = plt.subplots()

    ax.bar(x, values, width=1, edgecolor="white", linewidth=1)
    ax.set_ylabel("Number of clients")
    ax.set_title("Number of clients by gender")
    ax.set_xticks(x)
    ax.set_xticklabels(properties)

    fig.tight_layout()

    plt.show()


def number_of_restaurants_by_profile(dataset: DeliveryDataset) -> None:
    properties = ["FoodType.Pizza", "FoodType.HotDog", "FoodType.Soup", "FoodType.Hamburger", "FoodType.Sausage"]

    food_types = [
        FoodType.Pizza.name, FoodType.HotDog.name, FoodType.Soup.name, FoodType.Hamburger.name, FoodType.Sausage.name
    ]

    values = [0 for _ in food_types]

    for restaurant in dataset.restaurants:
        for food_type in food_types:
            if restaurant.profile == food_type:
                values[food_types.index(food_type)] += 1

    x = np.arange(len(properties))

    plt.style.use('_mpl-gallery')

    fig, ax = plt.subplots()

    ax.bar(x, values, width=1, edgecolor="white", linewidth=1)
    ax.set_ylabel("Number of restaurants")
    ax.set_title("Number of restaurants by FoodType")
    ax.set_xticks(x)
    ax.set_xticklabels(properties)

    fig.tight_layout()

    plt.show()
