-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-06-12 07:39:11
-- 伺服器版本： 10.4.27-MariaDB
-- PHP 版本： 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `social_medial`
--

-- --------------------------------------------------------

--
-- 資料表結構 `actions`
--

CREATE TABLE `actions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action_type` enum('view','like','comment','share') NOT NULL,
  `post_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `actions`
--

INSERT INTO `actions` (`id`, `user_id`, `action_type`, `post_id`, `timestamp`) VALUES
(4, 4, 'like', 17, '2025-06-06 23:52:21'),
(5, 5, 'like', 17, '2025-06-06 23:55:02'),
(6, 5, 'view', 17, '2025-06-07 00:02:14'),
(7, 5, 'view', 17, '2025-06-07 11:07:09'),
(8, 7, 'like', 17, '2025-06-07 20:24:57'),
(9, 7, 'comment', 13, '2025-06-07 21:03:41'),
(10, 7, 'like', 13, '2025-06-07 21:52:17'),
(11, 4, 'view', 4, '2025-06-08 00:41:54'),
(12, 4, 'view', 6, '2025-06-08 09:59:54'),
(13, 7, 'like', 13, '2025-06-08 14:49:51'),
(14, 7, 'view', 13, '2025-06-08 14:50:37'),
(15, 7, 'view', 17, '2025-06-08 14:56:27'),
(16, 4, 'view', 4, '2025-06-08 15:27:46'),
(17, 6, 'view', 13, '2025-06-08 15:45:54'),
(18, 4, 'view', 20, '2025-06-09 12:20:29'),
(19, 4, 'view', 62, '2025-06-09 12:21:20'),
(20, 4, 'view', 63, '2025-06-09 12:22:29'),
(21, 4, 'like', 64, '2025-06-09 12:22:36'),
(22, 4, 'like', 66, '2025-06-09 12:22:44'),
(23, 4, 'view', 58, '2025-06-09 12:29:23'),
(24, 4, 'view', 68, '2025-06-09 12:29:33'),
(25, 7, 'like', 18, '2025-06-09 12:30:31'),
(26, 7, 'like', 3, '2025-06-09 12:30:49'),
(27, 7, 'like', 7, '2025-06-09 12:31:59'),
(28, 7, 'view', 7, '2025-06-09 12:32:03'),
(29, 7, 'comment', 7, '2025-06-09 12:32:08'),
(30, 7, 'like', 51, '2025-06-09 12:33:10'),
(31, 7, 'view', 52, '2025-06-09 12:33:34'),
(32, 7, 'like', 30, '2025-06-09 12:40:45'),
(33, 7, 'like', 26, '2025-06-09 12:41:03'),
(34, 7, 'comment', 29, '2025-06-09 12:43:56'),
(35, 7, 'like', 23, '2025-06-09 12:45:21'),
(36, 7, 'view', 23, '2025-06-09 12:45:23'),
(37, 7, 'like', 55, '2025-06-09 13:05:25'),
(38, 7, 'like', 71, '2025-06-09 13:08:29'),
(39, 7, 'view', 71, '2025-06-09 13:08:30'),
(40, 7, 'view', 3, '2025-06-09 13:11:59'),
(41, 7, 'view', 30, '2025-06-09 13:36:05'),
(42, 7, 'view', 55, '2025-06-09 13:48:52'),
(43, 7, 'view', 29, '2025-06-09 13:59:16'),
(44, 7, 'view', 18, '2025-06-09 14:35:51'),
(45, 7, 'comment', 18, '2025-06-09 14:35:56'),
(46, 7, 'comment', 26, '2025-06-09 14:45:00'),
(47, 7, 'view', 26, '2025-06-09 14:45:22'),
(48, 7, 'comment', 51, '2025-06-09 14:55:03'),
(49, 7, 'view', 51, '2025-06-09 15:34:18'),
(50, 7, 'comment', 64, '2025-06-09 15:36:20'),
(51, 7, 'view', 64, '2025-06-09 15:36:34'),
(52, 7, 'like', 64, '2025-06-09 15:36:35'),
(53, 7, 'comment', 4, '2025-06-09 15:40:49'),
(54, 7, 'view', 4, '2025-06-09 15:41:33'),
(55, 7, 'like', 32, '2025-06-09 16:00:24'),
(56, 7, 'like', 46, '2025-06-09 16:07:17'),
(57, 7, 'comment', 20, '2025-06-09 16:47:18'),
(58, 7, 'view', 18, '2025-06-09 23:29:41'),
(59, 7, 'view', 26, '2025-06-09 23:35:36'),
(60, 7, 'comment', 18, '2025-06-09 23:36:11');

-- --------------------------------------------------------

--
-- 資料表結構 `blocks`
--

CREATE TABLE `blocks` (
  `id` int(11) NOT NULL,
  `blocker_id` int(11) NOT NULL,
  `blocked_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `is_deleted` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `comments`
--

INSERT INTO `comments` (`id`, `user_id`, `post_id`, `comment`, `parent_id`, `created_at`, `is_deleted`) VALUES
(4, 5, 13, 'Takodachi !!', NULL, '2025-06-05 12:22:26', 0),
(5, 5, 13, '這是新的內容', NULL, '2025-06-05 12:24:09', 0),
(6, 5, 13, 'Takodachi !!', NULL, '2025-06-05 12:24:28', 0),
(7, 5, 13, 'Takodachi !!', NULL, '2025-06-05 12:40:35', 0),
(8, 5, 13, 'Takodachi !!', NULL, '2025-06-05 21:10:59', 0),
(9, 5, 13, 'Takodachi !!', NULL, '2025-06-05 21:29:51', 0),
(10, 5, 13, 'Takodachi !!', NULL, '2025-06-05 21:40:20', 0),
(11, 5, 13, 'Takodachi !!', NULL, '2025-06-05 21:49:18', 0),
(12, 5, 13, 'ina 超讚', NULL, '2025-06-05 22:39:27', 0),
(13, 5, 13, 'ina 超讚', NULL, '2025-06-05 22:40:05', 0),
(14, 5, 13, '我來回覆這則留言', NULL, '2025-06-05 22:40:47', 0),
(15, 5, 13, '這是一則留言', NULL, '2025-06-05 22:42:07', 0),
(24, 4, 13, '喔耶喔耶', 4, '2025-06-06 12:18:03', 1),
(25, 7, 13, '你好', 5, '2025-06-07 21:03:41', 0),
(26, 7, 13, '真假', 5, '2025-06-07 21:52:53', 0),
(27, 7, 7, 'so cute', NULL, '2025-06-09 12:32:08', 1),
(28, 7, 29, '超棒', NULL, '2025-06-09 12:43:56', 0),
(29, 7, 29, '厲害', 28, '2025-06-09 13:59:16', 0),
(30, 7, 18, '真棒~', NULL, '2025-06-09 14:35:56', 0),
(31, 7, 18, '超棒', 30, '2025-06-09 14:36:04', 0),
(32, 7, 26, '超可愛', NULL, '2025-06-09 14:45:00', 0),
(33, 7, 51, '都機都機~', NULL, '2025-06-09 14:55:03', 1),
(34, 7, 51, '這則留言已被', 33, '2025-06-09 15:10:22', 1),
(35, 7, 51, '音速小子~~', NULL, '2025-06-09 15:32:24', 0),
(36, 7, 51, '都機都機', 35, '2025-06-09 15:32:39', 1),
(37, 7, 64, '真的', NULL, '2025-06-09 15:36:20', 0),
(38, 7, 4, '喔是喔', NULL, '2025-06-09 15:40:49', 0),
(39, 7, 20, '50元快剪', NULL, '2025-06-09 16:47:18', 0),
(40, 7, 18, '超可愛', 30, '2025-06-09 23:36:11', 0),
(41, 7, 18, '真的!!', 31, '2025-06-09 23:36:20', 0),
(42, 7, 18, '真的', 31, '2025-06-09 23:36:30', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `follows`
--

CREATE TABLE `follows` (
  `id` int(11) NOT NULL,
  `follower_id` int(11) NOT NULL,
  `followee_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ;

--
-- 傾印資料表的資料 `follows`
--

INSERT INTO `follows` (`id`, `follower_id`, `followee_id`, `created_at`) VALUES
(5, 5, 4, '2025-06-05 09:17:03'),
(12, 4, 5, '2025-06-08 10:00:12'),
(13, 7, 8, '2025-06-09 12:45:19');

-- --------------------------------------------------------

--
-- 資料表結構 `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `action_type` enum('like','dislike') DEFAULT 'like'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `likes`
--

INSERT INTO `likes` (`id`, `user_id`, `post_id`, `created_at`, `action_type`) VALUES
(7, 4, 17, '2025-06-06 23:52:47', 'like'),
(8, 5, 17, '2025-06-06 23:55:02', 'like'),
(11, 7, 17, '2025-06-07 21:30:14', 'like'),
(16, 7, 13, '2025-06-08 15:20:46', 'like'),
(17, 4, 64, '2025-06-09 12:22:36', 'like'),
(18, 4, 66, '2025-06-09 12:22:44', 'like'),
(19, 7, 18, '2025-06-09 12:30:31', 'like'),
(20, 7, 3, '2025-06-09 12:30:49', 'like'),
(22, 7, 51, '2025-06-09 12:33:10', 'like'),
(23, 7, 30, '2025-06-09 12:40:45', 'like'),
(24, 7, 26, '2025-06-09 12:41:03', 'like'),
(25, 7, 23, '2025-06-09 12:45:21', 'like'),
(27, 7, 71, '2025-06-09 13:08:29', 'like'),
(28, 7, 64, '2025-06-09 15:36:35', 'like'),
(29, 7, 32, '2025-06-09 16:00:24', 'like');

-- --------------------------------------------------------

--
-- 資料表結構 `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_hidden` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `posts`
--

INSERT INTO `posts` (`id`, `user_id`, `content`, `created_at`, `updated_at`, `is_hidden`) VALUES
(3, 4, 'Just returned from Kyoto! The temples were beautiful.', '2025-06-04 14:22:10', '2025-06-04 14:22:10', 0),
(4, 5, 'Made sushi for the first time. 🍣', '2025-06-04 14:22:10', '2025-06-04 14:22:10', 0),
(5, 4, 'Went hiking in Alishan. Nature is healing.', '2025-06-04 14:22:10', '2025-06-08 09:38:49', 0),
(6, 5, 'Bought a new gaming laptop. Time to grind.', '2025-06-04 14:22:10', '2025-06-04 14:22:10', 0),
(7, 4, 'My cat climbed into the laundry basket again. 😹 #cat', '2025-06-04 14:22:10', '2025-06-08 02:42:09', 0),
(8, 5, 'This is a test post from Postman', '2025-06-04 07:53:08', '2025-06-04 08:24:57', 1),
(13, 4, 'WAH #ina', '2025-06-04 10:24:51', '2025-06-06 16:16:12', 0),
(17, 4, 'ina 好可愛 #ina #可愛', '2025-06-06 08:12:49', '2025-06-06 08:20:30', 0),
(18, 4, 'ina 勇者服裝好可愛！ #ina', '2025-06-07 14:29:21', '2025-06-09 03:40:46', 0),
(19, 4, '生物資訊想法~', '2025-06-08 05:25:04', '2025-06-08 08:00:53', 1),
(20, 7, '剪了一顆呆瓜頭 #剪髮', '2025-06-08 06:08:28', '2025-06-08 06:25:19', 0),
(21, 8, '我的貓咪今天一整天都在打盹，好舒服啊！ #cat', '2025-06-01 08:00:00', '2025-06-01 08:00:00', 0),
(22, 8, '新領養了一隻小貓，牠叫「咪咪」 🐱', '2025-06-01 08:10:00', '2025-06-01 08:10:00', 0),
(23, 8, '看到貓咪追著毛線球真的太療癒了。 #貓咪 #可愛', '2025-06-01 08:20:00', '2025-06-09 04:40:24', 0),
(24, 8, '貓咪又把我的襪子叼走了...😼', '2025-06-01 08:30:00', '2025-06-01 08:30:00', 0),
(25, 8, '貓咪下午茶時間，準備了鮪魚罐頭。', '2025-06-01 08:40:00', '2025-06-01 08:40:00', 0),
(26, 8, '貓咪愛曬太陽，牠在陽臺上睡著了 ☀️ #貓咪 #可愛', '2025-06-01 08:50:00', '2025-06-09 04:40:08', 0),
(27, 8, '貓咪爬到書架上，真調皮！', '2025-06-01 09:00:00', '2025-06-01 09:00:00', 0),
(28, 8, '貓咪今天不肯吃飯，是不是肚子不舒服？', '2025-06-01 09:10:00', '2025-06-01 09:10:00', 0),
(29, 8, '和貓咪一起看電視，牠好像很有興趣。#貓咪 #可愛', '2025-06-01 09:20:00', '2025-06-09 04:39:56', 0),
(30, 8, '貓咪的爪子好迷人，柔軟又可愛！ #貓咪', '2025-06-01 09:30:00', '2025-06-09 04:39:40', 0),
(31, 9, '今天帶狗狗去散步，牠玩得好開心！ #dog', '2025-06-02 08:00:00', '2025-06-02 08:00:00', 0),
(32, 9, '狗狗學會了握手，好聰明！', '2025-06-02 08:10:00', '2025-06-02 08:10:00', 0),
(33, 9, '我的狗狗最喜歡吃雞肉。', '2025-06-02 08:20:00', '2025-06-02 08:20:00', 0),
(34, 9, '看到狗狗翻肚皮真是太可愛了～', '2025-06-02 08:30:00', '2025-06-02 08:30:00', 0),
(35, 9, '狗狗的新玩具球，到處跑來跑去。', '2025-06-02 08:40:00', '2025-06-02 08:40:00', 0),
(36, 9, '狗狗舔我的臉，好幸福啊！', '2025-06-02 08:50:00', '2025-06-02 08:50:00', 0),
(37, 9, '狗狗和貓咪第一次見面，妙趣橫生。', '2025-06-02 09:00:00', '2025-06-02 09:00:00', 0),
(38, 9, '狗狗的尾巴一直搖個不停～', '2025-06-02 09:10:00', '2025-06-02 09:10:00', 0),
(39, 9, '今天給狗狗洗澡，牠看起來很無辜。', '2025-06-02 09:20:00', '2025-06-02 09:20:00', 0),
(40, 9, '狗狗的耳朵好像米其林大師帽！ #狗 #可愛', '2025-06-02 09:30:00', '2025-06-09 08:08:28', 0),
(41, 10, '日本旅行第一天，去了東京塔。 #japan', '2025-06-03 08:00:00', '2025-06-03 08:00:00', 0),
(42, 10, '品嘗了道地的壽司，好美味！#壽司 #日本 #好吃', '2025-06-03 08:10:00', '2025-06-09 09:44:05', 0),
(43, 10, '漫步在京都的祇園街道，好有古風。', '2025-06-03 08:20:00', '2025-06-03 08:20:00', 0),
(44, 10, '在大阪的街頭買到超好吃的章魚燒。', '2025-06-03 08:30:00', '2025-06-03 08:30:00', 0),
(45, 10, '參觀了富士山，風景壯麗！', '2025-06-03 08:40:00', '2025-06-03 08:40:00', 0),
(46, 10, '泡了溫泉，整個人都放鬆了。', '2025-06-03 08:50:00', '2025-06-03 08:50:00', 0),
(47, 10, '在神社許了心願，感覺很神聖。', '2025-06-03 09:00:00', '2025-06-03 09:00:00', 0),
(48, 10, '搭乘新幹線，速度太快了！#日本 #旅行 # 新幹線', '2025-06-03 09:10:00', '2025-06-09 09:41:53', 0),
(49, 10, '購物狂歡，帶了好多紀念品。#購物 #旅行', '2025-06-03 09:20:00', '2025-06-09 09:42:17', 0),
(50, 10, '在秋葉原逛電子街，超酷！#動漫 #日本 #旅行', '2025-06-03 09:30:00', '2025-06-09 09:41:31', 0),
(51, 11, '今天跟他一起散步，心跳還是會加速。 #戀愛', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(52, 11, '原來喜歡一個人，是這種甜甜的感覺。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(53, 11, '下雨天和喜歡的人躲在同一把傘下，是浪漫的定義。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(54, 11, '他說晚安的語氣，比誰都溫柔。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(55, 11, '戀愛像糖果，有時太甜，有時會黏牙。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(56, 12, '水瓶座真的很怪，但怪得可愛！ #星座', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(57, 12, '巨蟹今天適合放鬆，不適合思考太多。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(58, 12, '金牛座的固執，是有原則的溫柔。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(59, 12, '今天月亮進入雙魚座，情緒特別豐富。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(60, 12, '你相信星座可以決定緣分嗎？我開始有點相信了。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(61, 13, '開了一整天會，我的靈魂已經飛走了。 #職場日記', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(62, 13, '上班時候像機器，下班只想癱在沙發。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(63, 13, '同事突然請假，所有工作都落我身上😢', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(64, 13, '最怕主管說「我有件小事想麻煩你」。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(65, 13, '午休時間是我最珍惜的自由。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(66, 14, '學會放下，是給自己最好的禮物。 #心靈成長', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(67, 14, '每天進步一點點，就會慢慢靠近更好的自己。#心靈成長', '2025-06-09 00:00:57', '2025-06-09 09:39:58', 0),
(68, 14, '停止與他人比較，你就是獨一無二的存在。#心靈成長', '2025-06-09 00:00:57', '2025-06-09 09:40:08', 0),
(69, 14, '情緒來了，就靜靜看著它，不評價。#心靈成長', '2025-06-09 00:00:57', '2025-06-09 09:40:03', 0),
(70, 14, '內心平靜，才是真的自由。', '2025-06-09 00:00:57', '2025-06-09 00:00:57', 0),
(71, 8, '貓好香 #貓咪', '2025-06-09 05:08:08', '2025-06-09 05:08:08', 0),
(72, 7, '要做不完了 今天要交....', '2025-06-09 05:57:07', '2025-06-09 05:58:54', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `post_images`
--

CREATE TABLE `post_images` (
  `id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `post_images`
--

INSERT INTO `post_images` (`id`, `post_id`, `image_path`) VALUES
(6, 13, 'post1_img2.jpg'),
(7, 13, 'post1_img1.jpg'),
(8, 17, 'ina.jpg'),
(10, 19, 's11159038_1.jpg');

-- --------------------------------------------------------

--
-- 資料表結構 `post_tags`
--

CREATE TABLE `post_tags` (
  `post_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `post_tags`
--

INSERT INTO `post_tags` (`post_id`, `tag_id`) VALUES
(3, 1),
(3, 6),
(4, 2),
(4, 6),
(5, 1),
(5, 3),
(5, 7),
(6, 4),
(7, 8),
(13, 9),
(17, 9),
(17, 10),
(18, 9),
(20, 11),
(23, 10),
(23, 12),
(26, 10),
(26, 12),
(29, 10),
(29, 12),
(30, 12),
(40, 10),
(40, 13),
(42, 15),
(42, 19),
(42, 20),
(48, 15),
(48, 16),
(49, 16),
(49, 18),
(50, 15),
(50, 16),
(50, 17),
(66, 14),
(67, 14),
(68, 14),
(69, 14),
(71, 12);

-- --------------------------------------------------------

--
-- 資料表結構 `recommend_logs`
--

CREATE TABLE `recommend_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `recommended_post_id` int(11) NOT NULL,
  `reward` float DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `role_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `roles`
--

INSERT INTO `roles` (`id`, `role_name`) VALUES
(1, 'admin'),
(2, 'regular'),
(3, 'moderator'),
(4, 'banned');

-- --------------------------------------------------------

--
-- 資料表結構 `tags`
--

CREATE TABLE `tags` (
  `id` int(11) NOT NULL,
  `tag_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `tags`
--

INSERT INTO `tags` (`id`, `tag_name`) VALUES
(8, 'cat'),
(2, 'food'),
(7, 'hiking'),
(9, 'ina'),
(6, 'japan'),
(3, 'nature'),
(5, 'pet'),
(4, 'tech'),
(1, 'travel'),
(11, '剪髮'),
(17, '動漫'),
(10, '可愛'),
(19, '壽司'),
(20, '好吃'),
(14, '心靈成長'),
(16, '旅行'),
(15, '日本'),
(13, '狗'),
(12, '貓咪'),
(18, '購物');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role_id`, `created_at`, `updated_at`) VALUES
(4, 'test', 'newuser@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-03 22:42:11', '2025-06-03 22:53:44'),
(5, 'admin', 'admin@example.com', 'scrypt:32768:8:1$waEx7kd6tZZSBnco$a518599e6f8de29f232ca006a004713782398f35b568f641fd5c6e5c639c026de15f57a08573963bdcce60cf3cb3f10e5773bf652de39f366d1f2e34a570d580', 1, '2025-06-03 22:54:17', '2025-06-04 16:23:24'),
(6, 'moderator', 'moderator@gmail.com', 'scrypt:32768:8:1$mRuhJXirhdNGESYU$a3991958baee3ff321fb72fa04ec4525b93021fcd98c0889e06c5bd51d54f2d61fa6b1269afe3814dc8a51f1a3d9b250754e89f016501e1df4925eb569410e1e', 3, '2025-06-07 12:57:08', '2025-06-07 12:57:08'),
(7, 'yoyo', 'yoyo@gmail.com', 'scrypt:32768:8:1$VnQWcvPLfKjEVfFx$9eaebf53a1e351a8c4299ff08fdc7cbb097f4f3d6716cbab7940adf130498f04ca7c9def9221fd542a6f8c35fff14df933706ea02515d120180ee19fb631cb2f', 2, '2025-06-07 15:08:44', '2025-06-08 16:31:50'),
(8, 'catlover', 'catlover@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-01 07:00:00', '2025-06-08 23:39:48'),
(9, 'doglover', 'doglover@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-02 07:00:00', '2025-06-08 23:39:48'),
(10, 'japantraveler', 'japantraveler@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-03 07:00:00', '2025-06-08 23:39:48'),
(11, 'romantic_soul', 'romance@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-09 00:00:56', '2025-06-09 00:00:57'),
(12, 'starchild', 'zodiac@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-09 00:00:56', '2025-06-09 00:00:57'),
(13, 'office_warrior', 'career@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-09 00:00:56', '2025-06-09 00:00:57'),
(14, 'mindgrower', 'growth@example.com', 'scrypt:32768:8:1$EDfM02mi74ckAvKq$cea83bc5aac7fb6ed906a6272f69eb8dda4f1f3f74896ead7993a9c89ca1a7d11951af09ce62a4a8e3b247042892c76bed58de1e63152f3988df29c3bab00742', 2, '2025-06-09 00:00:56', '2025-06-09 00:00:57');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `post_id` (`post_id`);

--
-- 資料表索引 `blocks`
--
ALTER TABLE `blocks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `blocker_id` (`blocker_id`,`blocked_id`);

--
-- 資料表索引 `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `parent_id` (`parent_id`),
  ADD KEY `idx_post_id` (`post_id`);

--
-- 資料表索引 `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `follower_id` (`follower_id`,`followee_id`),
  ADD KEY `idx_follower_id` (`follower_id`),
  ADD KEY `idx_followee_id` (`followee_id`);

--
-- 資料表索引 `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`post_id`),
  ADD KEY `post_id` (`post_id`),
  ADD KEY `idx_user_post` (`user_id`,`post_id`);

--
-- 資料表索引 `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- 資料表索引 `post_images`
--
ALTER TABLE `post_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `post_id` (`post_id`);

--
-- 資料表索引 `post_tags`
--
ALTER TABLE `post_tags`
  ADD PRIMARY KEY (`post_id`,`tag_id`),
  ADD KEY `tag_id` (`tag_id`);

--
-- 資料表索引 `recommend_logs`
--
ALTER TABLE `recommend_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `recommended_post_id` (`recommended_post_id`);

--
-- 資料表索引 `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tag_name` (`tag_name`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_email` (`email`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `actions`
--
ALTER TABLE `actions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `blocks`
--
ALTER TABLE `blocks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `follows`
--
ALTER TABLE `follows`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `posts`
--
ALTER TABLE `posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `post_images`
--
ALTER TABLE `post_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `recommend_logs`
--
ALTER TABLE `recommend_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `tags`
--
ALTER TABLE `tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `actions`
--
ALTER TABLE `actions`
  ADD CONSTRAINT `actions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `actions_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `comments` (`id`) ON DELETE SET NULL;

--
-- 資料表的限制式 `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followee_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `post_images`
--
ALTER TABLE `post_images`
  ADD CONSTRAINT `post_images_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `post_tags`
--
ALTER TABLE `post_tags`
  ADD CONSTRAINT `post_tags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `post_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `recommend_logs`
--
ALTER TABLE `recommend_logs`
  ADD CONSTRAINT `recommend_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `recommend_logs_ibfk_2` FOREIGN KEY (`recommended_post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE;

--
-- 資料表的限制式 `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
