/* eslint-disable @typescript-eslint/no-misused-promises */
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
const products = [
  {
    name: 'Grapes',
    price: 3.99,
    location: 'Produce Section',
    description: 'Fresh and juicy green grapes, perfect for snacking or adding to a fruit salad.',
    additionalInfo: 'Grapes are a great source of vitamins C and K.',
    image: null,
    inCart: false,
    done: false,
    rfid: "1a-2b-3c-4d"
  },
  {
    name: 'Whole Wheat Bread',
    price: 2.49,
    location: 'Bakery Aisle',
    description: 'Hearty whole wheat bread, sliced and ready for your favorite sandwiches.',
    additionalInfo: 'Ingredients include whole wheat flour, water, yeast, and salt.',
    image: null,
    inCart: false,
    done: false,
    rfid: "3e-4a-2c-1d"
  },
  {
    name: 'Laptop',
    price: 1249.99,
    location: 'Electronics Section',
    description: 'High-performance laptop with a 15-inch display, perfect for work and entertainment.',
    additionalInfo: 'Specs: Intel Core i7, 16GB RAM, 512GB SSD, NVIDIA GTX 1650.',
    image: null,
    inCart: false,
    done: false,
    rfid: "11-22-33-44"
  },
  {
    name: 'Organic Bananas',
    price: 0.59,
    location: 'Produce Section',
    description: 'Ripe organic bananas, ideal for baking or as a healthy snack.',
    additionalInfo: 'Bananas are rich in potassium and fiber.',
    image: null,
    inCart: false,
    done: false,
    rfid: "aa-bb-cc-dd"
  },
  {
    name: 'LED Light Bulbs',
    price: 7.99,
    location: 'Home Improvement Aisle',
    description: 'Energy-saving LED light bulbs with a lifespan of over 10,000 hours.',
    additionalInfo: '60W equivalent, non-dimmable, A19 E26 standard base.',
    image: null,
    inCart: false,
    done: false,
    rfid: "ee-ff-11-22"
  },
  {
    name: 'Ground Coffee',
    price: 8.99,
    location: 'Coffee Aisle',
    description: 'Rich and full-bodied ground coffee, perfect for starting your day.',
    additionalInfo: '100% Arabica beans, medium roast.',
    image: null,
    inCart: false,
    done: false,
    rfid: "44-33-22-11"
  },
  {
    name: 'Sparkling Water',
    price: 0.99,
    location: 'Beverages Aisle',
    description: 'Refreshing and bubbly sparkling water, with no added sugars or artificial flavors.',
    additionalInfo: 'Ingredients: Carbonated water.',
    image: null,
    inCart: false,
    done: false,
    rfid: "99-88-77-66"
  },
  {
    name: 'Almonds',
    price: 5.49,
    location: 'Snack Aisle',
    description: 'Crunchy and nutritious almonds, a perfect healthy snack.',
    additionalInfo: 'Almonds are a good source of protein, fiber, and healthy fats.',
    image: null,
    inCart: false,
    done: false,
    rfid: "55-44-33-22" 
  },
  {
    name: 'Toothpaste',
    price: 3.99,
    location: 'Personal Care Aisle',
    description: 'Fluoride toothpaste for strong and healthy teeth, with a fresh mint flavor.',
    additionalInfo: 'Helps prevent cavities, gingivitis, and plaque.',
    image: null,
    inCart: false,
    done: false,
    rfid: "12-12-12-12"
  },
  {
    name: 'Chicken Breasts',
    price: 9.99,
    location: 'Meat Section',
    description: 'Lean and tender chicken breasts, perfect for grilling or baking.',
    additionalInfo: 'Pack contains 4 chicken breasts, approximately 1.5 lbs.',
    image: null,
    inCart: false,
    done: false,
    rfid: "23-23-23-23"
  },
  {
    name: 'Tomato Sauce',
    price: 1.99,
    location: 'Pasta Aisle',
    description: 'Rich and flavorful tomato sauce, made with ripe tomatoes and a blend of herbs.',
    additionalInfo: 'Ingredients: Tomato, water, salt, onion, garlic, basil, oregano.',
    image: null,
    inCart: false,
    done: false,
    rfid: "34-34-34-34"
  },
  {
    name: 'Cheddar Cheese',
    price: 4.50,
    location: 'Dairy Aisle',
    description: 'Sharp and creamy cheddar cheese, perfect for sandwiches and cheese platters.',
    additionalInfo: 'Made from 100% cow’s milk.',
    image: null,
    inCart: false,
    done: false,
    rfid: "45-45-45-45"
  },
  {
    name: 'Multivitamin Gummies',
    price: 12.99,
    location: 'Health Supplements Aisle',
    description: 'Tasty multivitamin gummies for daily health and wellness support.',
    additionalInfo: 'Contains vitamins A, C, D, E, and Zinc.',
    image: null,
    inCart: false,
    done: false,
    rfid: "56-56-56-56"
  },
  {
    name: 'Yogurt',
    price: 0.99,
    location: 'Dairy Aisle',
    description: 'Creamy and delicious yogurt, with live cultures for digestive health.',
    additionalInfo: 'Ingredients: Milk, live yogurt cultures.',
    image: null,
    inCart: false,
    done: false,
    rfid: "67-67-67-67"
  },
  {
    name: 'Olive Oil',
    price: 10.99,
    location: 'Cooking Oils Aisle',
    description: 'Extra virgin olive oil, perfect for dressings and cooking.',
    additionalInfo: 'Cold-pressed, 100% pure olive oil.',
    image: null,
    inCart: false,
    done: false,
    rfid: "78-78-78-78"
  },
  {
    name: 'Paper Towels',
    price: 8.99,
    location: 'Household Supplies Aisle',
    description: 'Super absorbent paper towels, ideal for quick cleanups and spills.',
    additionalInfo: 'Pack contains 6 rolls, each with 120 2-ply sheets.',
    image: null,
    inCart: false,
    done: false,
    rfid: "89-89-89-89"
  },
  {
    name: 'Ice Cream',
    price: 4.99,
    location: 'Frozen Foods Aisle',
    description: 'Rich and creamy ice cream, available in a variety of flavors.',
    additionalInfo: 'Flavors: Vanilla, Chocolate, Strawberry, Mint Chocolate Chip.',
    image: null,
    inCart: false,
    done: false,
    rfid: "90-90-90-90"
  },
  {
    name: 'Socks',
    price: 9.99,
    location: 'Clothing Section',
    description: 'Comfortable and durable socks, perfect for everyday wear.',
    additionalInfo: 'Pack includes 5 pairs of assorted colors.',
    image: null,
    inCart: false,
    done: false,
    rfid: "ab-ab-ab-ab"
  },
  {
    name: 'Shampoo',
    price: 5.99,
    location: 'Personal Care Aisle',
    description: 'Nourishing shampoo for healthy and shiny hair, suitable for all hair types.',
    additionalInfo: 'Contains natural ingredients like aloe vera and coconut oil.',
    image: null,
    inCart: false,
    done: false,
    rfid: 'ce-67-01-02'
  },
  {
    name: 'Coffee Maker',
    price: 79.99,
    location: 'Electronics Section',
    description: 'Convenient and easy-to-use coffee maker, perfect for brewing your morning cup.',
    additionalInfo: 'Features include programmable settings, a pause-and-serve function, and a 12-cup capacity.',
    image: null,
    inCart: false,
    done: false,
    rfid: 'fa-95-f7-a8'
  }
];

  for (const product of products) {
    await prisma.product.create({
      data: product,
    });
  }
}

main()
  .catch(e => {
    throw e
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
