-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 29, 2023 at 05:36 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hoteltest`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminusers`
--

CREATE TABLE `adminusers` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `adminmail` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `verified` varchar(255) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adminusers`
--

INSERT INTO `adminusers` (`id`, `username`, `adminmail`, `password`, `verified`, `owner`) VALUES
(8, 'test', 'test@test.com', 'b10d98ac54c9a8a4', '0', '0'),
(9, 'siddhant', 'siddhant.hajare30@gmail.com', '6cd9d9ff318e4708', '1', '0'),
(11, 'asdasd', 'adityamondkar22@gmail.com', 'd3326f5ff814', '1', '0'),
(13, 'soham', 'crafterking@tutanota.com', '59dce6a41447', '0', '0'),
(16, 'admin', 'adityamondkar111@gmail.com', 'b1882020f107', '1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `allitems`
--

CREATE TABLE `allitems` (
  `item` varchar(225) DEFAULT NULL,
  `quantity` int(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `allitems`
--

INSERT INTO `allitems` (`item`, `quantity`) VALUES
('Espresso', 1),
('Samosa', 2),
('Vadapav', 1),
('Samosa', 1),
('Sandwich', 1),
('Vadapav', 1),
('Sandwich', 1),
('Latte', 1),
('Samosa', 2),
('Momos', 1);

-- --------------------------------------------------------

--
-- Table structure for table `beverages`
--

CREATE TABLE `beverages` (
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `imagelink` varchar(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `beverages`
--

INSERT INTO `beverages` (`user_id`, `title`, `description`, `imagelink`, `price`) VALUES
(2, 'Latte', 'A latte is a coffee beverage consisting of espresso, warm milk and a thin layer of foam. ', 'https://img.freepik.com/free-photo/latte-art-coffee-cup-cafe-table_1150-12132.jpg?size=626&ext=jpg', 149),
(3, 'Espresso', 'A strong, concentrated coffee made by forcing hot water through finely ground coffee beans.', 'https://img.freepik.com/free-photo/close-up-hands-barista-make-latte-coffee-art-paint_1150-12161.jpg?size=626&ext=jpg', 159),
(4, 'Cappuccino', 'An Italian coffee drink made with equal parts espresso, steamed milk, and milk foam.', 'https://img.freepik.com/free-photo/beautiful-fresh-relax-morning-coffee-cup-set_1150-7052.jpg?size=626&ext=jpg', 179),
(5, 'Black Coffee', 'It is made by brewing ground coffee beans with hot water, without adding any milk or cream.', 'https://img.freepik.com/premium-photo/coffee-cup-old-wooden-table-with-cream_158502-63.jpg?size=626&ext=jpg', 189),
(6, 'Chocolate Shake', 'A milkshake made with chocolate ice cream and chocolate syrup or chocolate powder', 'https://img.freepik.com/free-photo/creamy-vanilla-milky-shake-with-chocolate-sauce-white-saucer_114579-10109.jpg?size=626&ext=jpg', 199),
(7, 'Strawberry Shake', ' A milkshake made with strawberry ice cream and fresh or frozen strawberries.', 'https://img.freepik.com/premium-photo/milk-strawberry-cocktail_594857-354.jpg?size=626&ext=jpg', 149),
(8, 'Banana Shake', 'Banana shake is a creamy and sweet drink, made by blending ripe bananas, milk and ice together. ', 'https://img.freepik.com/free-photo/banana-almond-smoothie-dark-background_1150-45196.jpg?size=626&ext=jpg', 149),
(9, 'Oreo Shake', 'A milkshake made with Oreo cookies, either blended into the milkshake or used as a topping.', 'https://img.freepik.com/premium-photo/chocolate-milkshake-with-pieces-chocolate-chip-cookies_434193-2888.jpg?size=626&ext=jpg', 199),
(13, 'test', 'test', 'https://i.imgur.com/72KIfP8.jpeg', 100);

-- --------------------------------------------------------

--
-- Table structure for table `breakfast`
--

CREATE TABLE `breakfast` (
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `imagelink` varchar(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `breakfast`
--

INSERT INTO `breakfast` (`user_id`, `title`, `description`, `imagelink`, `price`) VALUES
(1, 'Vadapav', 'It consists of a deep-fried potato dumpling (vada) placed inside a bread roll (pav) and served with a variety of chutneys and spices.', 'https://img.freepik.com/free-photo/vada-pav-wada-pao-is-indian-desi-burger-is-roadside-fast-food-dish-from-maharashtra-selective-focus_466689-73963.jpg?size=626&ext=jpg', 29),
(2, 'Samosa', 'A samosa is a type of fried combination with a savory filling, such as spiced potatoes, onions, peas, chillies, & turmeric.', 'https://img.freepik.com/free-photo/samosa-singara-indian-fried-baked-pastry-with-savory-filling-spiced-potatoes-onion-peas_466689-90561.jpg?w=996&t=st=1674107362~exp=1674107962~hmac=bdcd120f8a891715a18919c6e35489c3ec7374c754ef1779fa242c860b8bb67d', 29),
(3, 'Momos', 'Momos are steamed dumpling. That have a filling of variety of meats, vegetables, cheese or only paneer. They are often served with a schzewan chutney & mayonnaise.', 'https://img.freepik.com/free-photo/tandoori-momo-veg-non-veg-red-cream-sauce-served-with-sauce-nepal-tibet-recipe_466689-90408.jpg?w=996&t=st=1674119295~exp=1674119895~hmac=df5680c8897511eaaef44699561278f6c85dd3be73b85d682e26a5d0804002f1', 119),
(4, 'Sandwich', 'A sandwich is a snack item consisting of vegetables, cheese, meat, or spread, placed on or between slices of bread. It is served with a green chutney & ketchup. ', 'https://img.freepik.com/free-photo/grilled-sandwich-with-bacon-fried-egg-tomato-lettuce-served-wooden-cutting-board_1150-42571.jpg?size=626&ext=jpg', 99),
(5, 'Doughnuts', 'Doughnuts are a sweet, deep-fried pastry made from dough. They are often topped with sugar or frosting, and can have fillings such as jelly or cream.', 'https://img.freepik.com/free-photo/fresh-tasty-donuts-with-chocolate-glaze_144627-881.jpg?size=626&ext=jpg', 179),
(6, 'Pancakes', 'Pancakes are a type of flat, round, and thin cake made from batter and cooked on a griddle or frying pan. And served with sweet syrup & berries.', 'https://img.freepik.com/premium-photo/stack-homemade-pancakes-with-fresh-berries_79782-328.jpg?size=626&ext=jpg', 199),
(7, 'Brownies', 'Brownies are a type of baked good that typically have a rich, chocolate flavor and a dense, fudgy texture. And it is served with vanilla ice-cream at the top.', 'https://img.freepik.com/free-photo/chocolate-brownie-served-with-vanilla-icecream-ball-strawberries_114579-2595.jpg?size=626&ext=jpg', 199),
(8, 'Cookies', 'A cookie is a small, flat, sweet baked good made from flour, sugar, and other ingredients such as butter or eggs. They are often sweet & crunchy, and comes in various flavors.', 'https://img.freepik.com/free-photo/chocolate-chip-cookie-white_93675-132144.jpg?size=626&ext=jpg', 69);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `item` varchar(255) DEFAULT NULL,
  `quantity` int(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL,
  `total` int(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `item`, `quantity`, `price`, `total`, `email`) VALUES
(14, 'Vadapav', 2, 29, 58, 'test@test.com'),
(15, 'Samosa', 2, 29, 58, 'test@test.com'),
(16, 'Oreo Shake', 2, 199, 398, 'test@test.com'),
(17, 'Soups', 1, 99, 99, 'test@test.com'),
(18, 'Chicken Biryani', 2, 219, 438, 'test@test.com'),
(139, 'Latte', 4, 149, 596, 'test1@test.com'),
(140, 'Espresso', 1, 159, 159, 'test1@test.com'),
(141, 'Cappuccino', 1, 179, 179, 'test1@test.com'),
(142, 'Black Coffee', 1, 189, 189, 'test1@test.com');

-- --------------------------------------------------------

--
-- Table structure for table `emailauth`
--

CREATE TABLE `emailauth` (
  `id` int(11) NOT NULL,
  `mail_default_sender` varchar(255) DEFAULT NULL,
  `mail_server` varchar(255) DEFAULT NULL,
  `mail_port` int(100) DEFAULT NULL,
  `mail_tls` varchar(255) DEFAULT NULL,
  `mail_ssl` varchar(255) DEFAULT NULL,
  `mail_username` varchar(255) DEFAULT NULL,
  `mail_password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `emailauth`
--

INSERT INTO `emailauth` (`id`, `mail_default_sender`, `mail_server`, `mail_port`, `mail_tls`, `mail_ssl`, `mail_username`, `mail_password`) VALUES
(1, 'Vintage Cafe <emailfortestpurpose0@gmail.com>', 'test', 465, 'test', 'test', 'test', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`user_id`, `name`, `email`, `password`) VALUES
(2, 'Anshul', 'anshukawale1080@gmail.com', 'vintage@123'),
(3, 'Aditya ', 'adityamondkar111@gmail.com', 'test'),
(7, 'Atharva', 'atharvamondkar111@gmail.com', 'atharvamondkar111@gmail.com'),
(12, 'Siddhant', 'Siddhant.hajare30@gmail.com', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `lunch`
--

CREATE TABLE `lunch` (
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `imagelink` varchar(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lunch`
--

INSERT INTO `lunch` (`user_id`, `title`, `description`, `imagelink`, `price`) VALUES
(2, 'Chicken Biryani', 'It is typically made with long-grain rice, marinated chicken, and a blend of aromatic spices, cooked together to create a flavorful and fragrant dish.', 'https://img.freepik.com/free-photo/indian-chicken-biryani-served-terracotta-bowl-with-yogurt-white-background-selective-focus_466689-72554.jpg?size=626&ext=jpg', 219),
(3, 'Pizza', 'Pizza is an oven-baked, flat, round bread typically topped with tomato sauce, cheese, and various toppings such as meat, vegetables, and herbs.', 'https://img.freepik.com/free-photo/mixed-pizza-with-various-ingridients_140725-3790.jpg?w=996&t=st=1674195616~exp=1674196216~hmac=e5b71fdb504b85288d3b8592609eedba0750cc1614fbbfa744bbec262782320f', 199),
(4, 'Soups', 'Soup is a dish, typically made by combining ingredients such as vegetables, meat, grains, and legumes in a pot. ', 'https://img.freepik.com/free-photo/tomato-soup-with-green-table_140725-2447.jpg?auto=format&h=200', 99),
(5, 'Burger', ' It is often garnished with cheese, lettuce, tomato, onion, pickles, and various condiments such as ketchup, mustard, and mayonnaise. ', 'https://img.freepik.com/free-photo/front-view-meat-burger-with-cheese-salad-tomatoes-dark-desk_140725-89522.jpg?w=996&t=st=1674195927~exp=1674196527~hmac=f2ac430c2b0ca5a7c3c508f2ed0a6d95c6206b68fccebf9c476b43ba4ac2849f', 149),
(6, 'Tacos', 'A taco is a traditional Mexican dish made of a corn or wheat tortilla folded or rolled around a filling, typically of meat, cheese, beans, or vegetables.', 'https://img.freepik.com/free-photo/mexican-tacos-with-beef-tomato-sauce-salsa_2829-14218.jpg?size=626&ext=jpg', 149),
(7, 'Paneer Tikka', 'It is made by marinating small cubes of Paneer (a type of Indian cottage cheese) in a mixture of yogurt and spices, before grilling or roasting. ', 'https://img.freepik.com/free-photo/chicken-skewers-with-slices-apples-chili_2829-19992.jpg?size=626&ext=jpg', 199),
(8, 'Tandoori Chicken', 'Tandoori chicken is a popular dish made by marinating chicken in a mixture of yogurt, spices and lemon juice before cooking in a tandoor oven.', 'https://img.freepik.com/free-photo/delicious-chicken-table_144627-8758.jpg?size=626&ext=jpg', 249),
(9, 'Pav Bhaji', ' It\'s a thick vegetable curry made of mixed vegetables cooked in spices and butter, served with a soft bread roll (pav) and garnished with coriander and butter. ', 'https://img.freepik.com/free-photo/pav-bhaji-is-fast-food-dish-from-india-consisting-thick-vegetable-curry-served-with-soft-bread-roll_466689-74257.jpg?size=626&ext=jpg', 129);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `item` varchar(255) DEFAULT NULL,
  `price` int(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `stripeid` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `tableno` int(255) DEFAULT NULL,
  `served` int(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `item`, `price`, `email`, `stripeid`, `date`, `note`, `tableno`, `served`, `name`) VALUES
(1, '[\'Espresso\']', 159, 'adityamondkar111@gmail.com', 'cs_test_a1r4LHaWb5tt04BHpkzwpX8v9kCEQAy0gDz4ZkZd6dgN65GlfOLDAMmgrh', '2023-04-17', '', 5, 1, 'Aditya '),
(2, '[\'Samosa\', \'Vadapav\']', 87, 'adityamondkar111@gmail.com', 'cs_test_a1jkuSqz3z53ZJlgP8MpKsTEQGVsp1laJAj9WAoKmgLxb7E0OuET57VnGa', '2023-04-19', '', 5, 1, 'Aditya '),
(3, '[\'Samosa\', \'Sandwich\']', 128, 'adityamondkar111@gmail.com', 'cs_test_a1qEFTTFpcS5nPFEU0s45MZZO3I4aSE7YYxBy3OrS0wq3Y0xYYdnSpc6UL', '2023-04-20', '', 2, 1, 'Aditya '),
(4, '[\'Vadapav\']', 29, 'anshukawale1080@gmail.com', 'cs_test_a1yOhXofgXoDLN4knflnYhNoUZsftBKdwpR1TVkGCoVsmevrUbKUeWqoK3', '2023-04-19', 'Green Chutney', 5, 2, 'Anshul'),
(8, '[\'Sandwich\']', 99, 'adityamondkar111@gmail.com', 'cs_test_a16jViMvKKPz46Gk2u04adqt8p2LJgKNAqEplOMk32Qt4wEfvDeZtDo74d', '2023-06-29', 'no tomato', 5, 2, 'Aditya '),
(9, '[\'Latte\']', 149, 'adityamondkar111@gmail.com', 'cs_test_a1Ze1JKR6V3yrarg5Yyx8p7sWmS5VsZWy5Lig7OUs494O4d7edmBSEBOD9', '2023-07-11', 'abc', 1212, 1, 'Aditya '),
(10, '[\'Samosa\', \'Momos\']', 177, 'adityamondkar111@gmail.com', 'cs_test_a10JP4SQzyxGqyY6QRNpH1ARUnkrAYQM25dFAXeldJWAwClQt6vVcDOvGF', '2023-07-29', '', 12, 1, 'Aditya ');

-- --------------------------------------------------------

--
-- Table structure for table `stripekeys`
--

CREATE TABLE `stripekeys` (
  `id` int(11) NOT NULL,
  `apikey` varchar(255) DEFAULT NULL,
  `pubkey` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stripekeys`
--


--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminusers`
--
ALTER TABLE `adminusers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `beverages`
--
ALTER TABLE `beverages`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `breakfast`
--
ALTER TABLE `breakfast`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `emailauth`
--
ALTER TABLE `emailauth`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `lunch`
--
ALTER TABLE `lunch`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stripekeys`
--
ALTER TABLE `stripekeys`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adminusers`
--
ALTER TABLE `adminusers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `beverages`
--
ALTER TABLE `beverages`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `breakfast`
--
ALTER TABLE `breakfast`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=231;

--
-- AUTO_INCREMENT for table `emailauth`
--
ALTER TABLE `emailauth`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `lunch`
--
ALTER TABLE `lunch`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `stripekeys`
--
ALTER TABLE `stripekeys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
