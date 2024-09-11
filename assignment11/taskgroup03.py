import time
import asyncio
from asyncio import Queue, TaskGroup

class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time

class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products

async def checkout_customer(queue: Queue, cashier_number: int):
    customer_count = 0
    total_checkout_time = 0.0
    cashier_stats = []
    
    while not queue.empty():
        customer: Customer = await queue.get()
        customer_start_time = time.perf_counter()
        print(f"The Cashier_{cashier_number} will checkout Customer_{customer.customer_id}")
        
        for product in customer.products:
            print(f"The Cashier_{cashier_number} will checkout Customer_{customer.customer_id}'s Product_{product.product_name} in {product.checkout_time} secs")
            await asyncio.sleep(product.checkout_time)
        
        checkout_time = round(time.perf_counter() - customer_start_time, ndigits=2)
        total_checkout_time += checkout_time
        customer_count += 1
        cashier_stats.append(checkout_time)
        
        print(f"The Cashier_{cashier_number} finished checkout Customer_{customer.customer_id} in {checkout_time} secs")
        queue.task_done()

    return {
        'cashier_number': cashier_number,
        'customers': customer_count,
        'times': cashier_stats,
        'total_time': round(total_checkout_time, ndigits=2)
    }

def generate_customer(customer_id: int) -> Customer:
    all_products = [Product('beef', 1),
                    Product('banana', .4),
                    Product('sausage', .4),
                    Product('diapers', .2)]
    return Customer(customer_id, all_products)

async def customer_generation(queue: Queue, customers: int):
    customer_count = 0
    while True:
        customers = [generate_customer(the_id) for the_id in range(customer_count, customer_count + customers)]
        
        for customer in customers:
            print("Waiting to put customer in line....")
            await queue.put(customer)
            print("Customer put in line...")
        
        customer_count += len(customers)
        await asyncio.sleep(0.001)
        return customer_count

async def main():
    customer_queue = Queue(5)
    customers_start_time = time.perf_counter()
    stats = {}
    
    async with TaskGroup() as tg:
        # Start customer generation
        tg.create_task(customer_generation(customer_queue, 2))
        
        # Start cashier tasks
        cashier_tasks = [tg.create_task(checkout_customer(customer_queue, i)) for i in range(2)]
    
    # Collect results from cashier tasks
    cashier_results = await asyncio.gather(*cashier_tasks)
    
    # Populate the stats dictionary from the results
    for result in cashier_results:
        stats[result['cashier_number']] = {
            'customers': result['customers'],
            'times': result['times'],
            'total_time': result['total_time']
        }
    
    # Display stats
    for cashier_number, stat in stats.items():
        print(f"Cashier_{cashier_number}: Customers = {stat['customers']}, Total Time = {stat['total_time']}s")
        print(f"  Times per customer: {stat['times']}")

    print(f"The supermarket process finished in {round(time.perf_counter() - customers_start_time, ndigits=2)} secs")

if __name__ == "__main__":
    asyncio.run(main())
