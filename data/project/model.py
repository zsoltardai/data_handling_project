from __future__ import annotations
from dataclasses import field, dataclass
import random
from typing import Type, cast
from faker import Faker
from data.project.base import Dataset, Entity
from enum import Enum
from uuid import uuid4


@dataclass
class DeliveryDataset(Dataset):
    people: list[Person]
    couriers: list[Courier]
    restaurants: list[Restaurant]
    orders: list[Order]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, Courier, Restaurant, Order]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return DeliveryDataset(
            cast(list[Person], entities[0]),
            cast(list[Courier], entities[1]),
            cast(list[Restaurant], entities[2]),
            cast(list[Order], entities[3])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[Courier] = self.couriers
        res[Restaurant] = self.restaurants
        res[Order] = self.orders

        return res

    @staticmethod
    def generate(
            count_of_people: int,
            count_of_couriers: int,
            count_of_restaurants: int,
            count_of_orders: int) -> DeliveryDataset:

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(
                    Person(
                        id="P-" + (str(i).zfill(6)),
                        name=generator.name_male() if male else generator.name_female(),
                        age=random.randint(min_age, max_age),
                        male=male,
                        address=generator.address()
                    )
                )

            return people

        def generate_couriers(number_of_couriers: int, male_ratio: float = 0.5, locale: str = "hu_HU",
                             unique: bool = False) -> list[Courier]:
            assert number_of_couriers > 0
            assert 0 < male_ratio < 1

            fake = Faker(locale)
            generator = fake.unique if unique else fake

            delivery_methods: list[DeliveryMethod] = [DeliveryMethod.Bicycle, DeliveryMethod.Car,
                                                      DeliveryMethod.Motorcycle]

            couriers = []

            for i in range(number_of_couriers):
                male = random.random() < male_ratio
                couriers.append(
                    Courier(
                        courier_id=str(uuid4()),
                        name=generator.name_male() if male else generator.name_female(),
                        age=random.randint(18, 40),
                        male=male,
                        delivery_method=str(random.choice(delivery_methods).name)
                    )
                )

            return couriers

        def generate_restaurants(number_of_restaurants: int,locale: str = "hu_HU",
                                 unique: bool = False,) -> list[Restaurant]:
            assert number_of_restaurants > 0

            fake = Faker(locale)
            generator = fake.unique if unique else fake

            profiles: list[FoodType] = [FoodType.Soup, FoodType.Pizza, FoodType.HotDog,
                                        FoodType.Hamburger, FoodType.Sausage]

            restaurants = []

            for i in range(number_of_restaurants):
                restaurants.append(
                    Restaurant(
                        restaurant_id=str(uuid4()),
                        name=f'{generator.company()} restaurant',
                        address=generator.address(),
                        phone_number=generator.phone_number(),
                        profile=str(random.choice(profiles).name)
                    )
                )

            return restaurants

        def generate_orders(number_of_orders: int, people: list[Person], couriers: list[Courier],
                            restaurants: list[Restaurant]) -> list[Order]:
            assert number_of_orders > 0
            assert len(people) > 0
            assert len(couriers) > 0
            assert len(restaurants) > 0

            orders = []

            for i in range(number_of_orders):
                person = random.choice(people)
                courier = random.choice(couriers)
                restaurant = random.choice(restaurants)

                amount_ordered = random.randint(1, 5)

                prices: dict[str, int] = {
                    FoodType.Soup.name: 7,
                    FoodType.Pizza.name: 10,
                    FoodType.HotDog.name: 5,
                    FoodType.Hamburger.name: 8,
                    FoodType.Sausage.name: 3
                }

                orders.append(
                    Order(
                        order_id=f"ORDER-{str(i).zfill(10)}",
                        amount=amount_ordered,
                        food_type=restaurant.profile,
                        restaurant_id=restaurant.restaurant_id,
                        restaurant_name=restaurant.name,
                        delivery_fee=(prices.get(restaurant.profile) * amount_ordered),
                        destination=person.address,
                        client_name=person.name,
                        client_id=person.id,
                        courier_id=courier.courier_id
                    )
                )

            return orders

        people = generate_people(count_of_people)
        couriers = generate_couriers(count_of_couriers)
        restaurants = generate_restaurants(count_of_restaurants, unique=True)
        orders = generate_orders(count_of_orders, people, couriers, restaurants)
        return DeliveryDataset(people, couriers, restaurants, orders)


@dataclass
class Order(Entity):
    order_id: str = field(hash=True)
    amount: int = field(repr=True, compare=False)
    food_type: str = field(repr=True, compare=False)
    restaurant_id: str = field(repr=True, compare=False)
    restaurant_name: str = field(repr=True, compare=False)
    delivery_fee: int = field(repr=True, compare=False)
    destination: str = field(repr=True, compare=False)
    client_name: str = field(repr=True, compare=False)
    client_id: str = field(repr=True, compare=False)
    courier_id: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Order:
        return Order(seq[0], int(seq[1]), seq[2], seq[3], seq[4], int(seq[5]), seq[6], seq[7], seq[8], seq[9])

    def to_sequence(self) -> list[str]:
        return [self.order_id, str(self.amount), str(self.food_type), self.restaurant_id, self.restaurant_name,
                str(self.delivery_fee), self.destination, self.client_name, self.client_id, self.courier_id]

    @staticmethod
    def field_names() -> list[str]:
        return ["order_id", "amount", "food_type", "restaurant_id", "restaurant_name", "delivery_fee", "destination",
                "client_name", "client_id", "courier_id"]

    @staticmethod
    def collection_name() -> str:
        return "orders"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Order.collection_name()} (
            order_id VARCHAR(50) NOT NULL PRIMARY KEY,
            amount INTEGER NOT NULL,
            food_type VARCHAR(50) NOT NULL,
            restaurant_id VARCHAR(50) NOT NULL,
            restaurant_name VARCHAR(50) NOT NULL,
            delivery_fee VARCHAR(50) NOT NULL,
            destination VARCHAR(50) NOT NULL,
            client_name VARCHAR(50) NOT NULL,
            client_id VARCHAR(100) NOT NULL,
            courier_id VARCHAR(50) NOT NULL,

            FOREIGN KEY (courier_id) REFERENCES {Courier.collection_name()}(courier_id),
            FOREIGN KEY (client_id) REFERENCES {Person.collection_name()}(id),
            FOREIGN KEY (restaurant_id) REFERENCES {Restaurant.collection_name()}(restaurant_id)
        );
         """


@dataclass
class Restaurant(Entity):
    restaurant_id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    address: str = field(repr=True, compare=False)
    phone_number: str = field(repr=True, compare=False)
    profile: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Restaurant:
        return Restaurant(seq[0], seq[1], seq[2], seq[3], seq[4])

    def to_sequence(self) -> list[str]:
        return [self.restaurant_id, self.name, self.address, self.phone_number, self.profile]

    @staticmethod
    def field_names() -> list[str]:
        return ["restaurant_id", "name", "address", "phone_number", "profile"]

    @staticmethod
    def collection_name() -> str:
        return "restaurants"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Restaurant.collection_name()} (
            restaurant_id VARCHAR(50) NOT NULL PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(100),
            phone_number VARCHAR(50),
            profile VARCHAR(50)
        );
        """


@dataclass
class Courier(Entity):
    courier_id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(repr=True, compare=False)
    delivery_method: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Courier:
        return Courier(seq[0], seq[1], int(seq[2]), bool(seq[3]), seq[4])

    def to_sequence(self) -> list[str]:
        return [self.courier_id, self.name, str(self.age), str(int(self.male)), self.delivery_method]

    @staticmethod
    def field_names() -> list[str]:
        return ["courier_id", "name", "age", "male", "delivery_method"]

    @staticmethod
    def collection_name() -> str:
        return "couriers"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Courier.collection_name()} (
            courier_id VARCHAR(50) NOT NULL PRIMARY KEY,
            name VARCHAR(100),
            age INTEGER,
            male BOOLEAN,
            delivery_method VARCHAR(50)
        );
        """


@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    address: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], seq[2], int(seq[3]), bool(seq[4]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, self.address, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "address", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(50) NOT NULL PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(100),
            age INTEGER,
            male BOOLEAN
        );
        """


class FoodType(Enum):
    Pizza = 'Pizza'
    Soup = 'Soup'
    Hamburger = 'Hamburger'
    HotDog = 'HotDog'
    Sausage = 'Sausage'


class DeliveryMethod(Enum):
    Bicycle = 'Bicycle'
    Motorcycle = 'Motorcycle'
    Car = 'Car'
