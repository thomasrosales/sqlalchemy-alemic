import random

from faker import Faker

from database.controllers import (
    create_user,
    get_user_by_id,
    add_order,
    add_product,
    add_product_to_order, select_all_user_orders, get_total_number_of_orders, get_total_number_order_filter_by,
)


def seed_fake_data():
    Faker.seed(0)
    fake = Faker()

    users = []
    orders = []
    products = []
    for _ in range(50):
        referrer_id = None if not users else users[-1].id
        user = create_user(
            name=fake.name(),
            last_name=fake.last_name(),
            emails=[fake.email()],
            referrer_id=referrer_id,
        )
        users.append(user)

    for _ in range(10):
        order = add_order(random.choice(users).id)
        orders.append(order)

    for _ in range(10):
        product = add_product(
            title=fake.word(),
            description=fake.sentence(),
            # price=fake.pyint()
        )
        products.append(product)

    for order in orders:
        for _ in range(3):
            add_product_to_order(
                order_id=order.id,
                product_id=random.choice(products).id,
                quantity=fake.pyint(),
            )


if __name__ == "__main__":
    for row in select_all_user_orders(10):
        # Product, Order, User.name, OrderProduct.quantity
        print(f"Products: {row[0].title}")
        print(f"Order: {row[1].id}")
        print(f"User: {row[2]}")
        print(f"Quantity: {row[3]}")

    num_orders = get_total_number_of_orders()
    print(num_orders)
    print(get_total_number_order_filter_by())
    # seed_fake_data()
