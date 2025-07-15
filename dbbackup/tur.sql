mysqldump: Deprecated program name. It will be removed in a future release, use '/opt/bitnami/mariadb/bin/mariadb-dump' instead
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tur
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `tur_chat_history`
--

DROP TABLE IF EXISTS `tur_chat_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_chat_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `chat_session_id` bigint(20) NOT NULL COMMENT '会话ID',
  `sender` enum('ai','user') DEFAULT NULL COMMENT '发送者',
  `text` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文本',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `chat_session_id` (`chat_session_id`) USING BTREE,
  CONSTRAINT `tur_chat_history_ibfk_1` FOREIGN KEY (`chat_session_id`) REFERENCES `tur_chat_sessions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_chat_history`
--

LOCK TABLES `tur_chat_history` WRITE;
/*!40000 ALTER TABLE `tur_chat_history` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_chat_history` VALUES
(1093,1,246,'user','你能帮我写一首歌吗？关于霸王别姬的','2025-07-15 05:55:17'),
(1094,1,246,'ai','当然可以！下面是一首简短的歌词，以霸王别姬的故事为背景，表达了项羽与虞姬间的情感和结局。\n\n【歌名】《临江别》\n\n【副歌】\n在霸王临江的地方，\n红尘中最后一舞尽伤。\n风雪里一曲唱离别章，\n剑影里血染长裳。\n\n【第一节】\n月下你轻抚琴弦，\n“虞兮虞兮，奈若何。”\n你的泪落在琴边，\n眼中尽是无尽思念。\n那日战旗翻飞如海，\n你翩然落马悲歌中。\n\n【副歌】\n在霸王临江的地方，\n红尘中最后一舞尽伤。\n风雪里一曲唱离别章，\n剑影里血染长裳。\n\n【第二节】\n英雄泪眼中刀光，\n“纵使前路千重浪。”\n月色下你轻抚我脸庞，\n却难改这苍茫过往。\n四面楚歌，血泪满场，\n你翩然落马悲歌唱飞荡。\n\n【副歌】\n在霸王临江的地方，\n红尘中最后一舞尽伤。\n风雪里一曲唱离别章，\n剑影里血染长裳。\n\n【桥段】\n江山如画，英雄未老，\n奈何终是两世迢遥。\n那一抹嫣红在时光流转中消逝，\n如今只剩这江水滔滔不绝。\n\n【副歌2】\n在霸王临江的地方，\n独望天边云翻月黄。\n风雪里一曲唱离别章，\n剑影里，爱与死长伴旁。\n\n【尾声】\n那一年花开半夏时分，\n如今你我隔世沉沦。\n纵使长夜漫漫路难寻，\n只愿来生再续今世情深。\n\n请注意，这首歌只是从“霸王别姬”的故事中汲取灵感编写的一首抒情歌曲。希望你喜欢！','2025-07-15 05:55:23'),
(1095,1,246,'user','hiphop','2025-07-15 05:56:00'),
(1096,1,246,'ai','当然可以！为了契合《霸王别姬》的故事背景和情感色彩，我们可以创作一首充满力量与情感的Hip-hop风格的歌词。\n\n【歌名】：《永恒之誓》\n\n【第一节】\n大风起兮云飞扬，\n一卷历史在胸膛。\n四面楚歌，剑影闪亮，\n心中有梦，肝胆相向。\n\n你在乌江边挥手别往，\n“虞姬，生如夏花，死如明月光。”\n你的笑映照我心上，\n万军之中，你独美难忘。\n\n【副歌】\n霸王别姬，血染疆场，\n悲壮绝唱，爱与离愁长。\n乌骓马嘶，剑影闪烁，\n你我一诺千金重！\n\n【第二节】\n霸王挥手，江山如画，\n六宫粉黛，终归尘沙。\n虞姬轻柔，泪眼相望，\n“明日黄花，为君再绽放。”\n\n但愿苍天有眼，\n明月依旧照亮那片天地。\n英雄泪湿战袍上，\n你我情深似海长。\n\n【桥段】\n在那临江的夜晚，\n琴弦低鸣，歌泣千行。\n爱与恨交错缠绵，\n你的悲歌未尽，我的梦仍在延续。\n\n【副歌】\n霸王别姬，血染疆场，\n悲壮绝唱，爱与离愁长。\n乌马嘶鸣，剑影闪烁，\n你我一诺千金重！\n\n【尾声】\n江水悠悠，岁月如梭，\n回忆中依稀可辨的你。\n英雄未老，爱意永恒，\n在历史的长河深处，我们永不忘。\n\n希望这段歌词能贴近你的需求。如果有任何调整或修改意见，请随时告诉我！','2025-07-15 05:56:05'),
(1097,1,246,'user','rapper','2025-07-15 05:56:08'),
(1098,1,246,'ai','好的，我们将为《霸王别姬》的故事创造一段hip-hop风格的歌词，以rap的形式来表达情感和剧情。以下是创作的一段歌词：\n\n【歌名】：《霸王别姬》\n\n[Bridge & Chorus]\n在乌江之畔，风萧夜静，\n霸王挥剑，别姬轻声。\n霸王豪情万丈，美人柔肠千转，\n在这历史的长卷，爱恨交织难断。\n\n[Verse 1 - Rapper: 正义者]\n四面楚歌响彻天边，\n金戈铁马血如泉。\n你在帷幕后低吟浅唱，\n我手中握剑，豪情难掩。\n\n战场风云变幻无常，\n英雄泪湿衣裳上。\n虞姬柔情似水长流，\n誓与君王生死相望。\n\n[Verse 2 - Rapper: 爱人]\n四面楚歌中，你独步辉煌，\n红颜一笑，倾覆江山。\n那日月下，琴声悠扬，\n我独守那份承诺绵延。\n\n乌江边挥手一别，\n泪眼含烟雾弥漫。\n纵使刀光剑影间，\n爱恋如铁血满腔。\n\n[Chorus]\n霸王别姬，英雄悲歌奏响，\n虞姬轻盈，泪湿长裳。\n乌马嘶鸣剑光闪烁，\n誓言刻骨，难舍难忘。\n\n[Bridge & Chorus (重复)]\n在乌江之畔，风萧夜静，\n霸王挥剑，别姬轻声。\n霸王豪情万丈，美人柔肠千转，\n在这历史的长卷，爱恨交织难断。\n\n[Verse 3 - Rapper: 正义者]\n四面楚歌中你英姿不减，\n誓死守卫这份人间绝恋。\n刀光剑影下，你一舞倾城，\n愿与君王共赴黄泉路长。\n\n乌江边别离依依不舍，\n但愿来世再续前缘。\n英雄泪湿衣裳上，\n爱恋如铁血满腔。\n\n[Outro - Rapper: 爱人]\n历史的长河悠悠流去，\n你我情深似海长。\n霸王别姬，永不止息，\n在心中那份永恒之誓，铭记在心。\n\n希望这段歌词能够符合你的要求。如果有任何调整或修改意见，请随时告诉我！','2025-07-15 05:56:14'),
(1099,1,246,'user','good','2025-07-15 05:56:17'),
(1100,1,246,'ai','太好了！很高兴你喜欢这首《霸王别姬》的Hip-hop风格歌词。如果你有任何其他需求或者想要进一步完善和修改的地方，欢迎随时告诉我！\n\n如果需要制作音乐、寻找合作者或者是进行其他的创作活动，我也很乐意提供帮助。祝你的创作顺利！\n\n如果有更多的内容或问题，我们继续交流吧！','2025-07-15 05:56:18'),
(1101,1,246,'user','sdf','2025-07-15 05:56:18'),
(1102,1,246,'ai','看起来你输入了一些随机的字符。如果你有任何具体的问题或者需要进一步的帮助，请告诉我！我可以继续帮你在写歌词、提供信息或者其他方面的支持。','2025-07-15 05:56:19'),
(1103,1,246,'user','写一篇作文','2025-07-15 05:56:26'),
(1104,1,246,'ai','当然可以！请告诉我你想要写作的主题或内容是什么？例如，你是想要写一篇关于《霸王别姬》的故事分析，还是希望探讨项羽和虞姬之间的感情？或者有其他特定的要求或主题吗？\n\n如果没有具体要求，我可以帮你写一篇简短的作文，以《霸王别姬》为主题，探讨这段历史故事及其对现代人的启示。\n\n以下是示例作文：\n\n---\n\n**霸王别姬：一段千古悲歌**\n\n在古代的历史长河中，有许多令人难忘的故事。其中，《霸王别姬》不仅是项羽和虞姬之间的爱情传说，更是中华文化中浓墨重彩的一笔。这篇作文将从故事背景、人物情感以及现代启示三个方面来探讨这一段充满悲剧色彩的英雄爱情。\n\n### 故事背景\n《霸王别姬》源于中国古代历史中的楚汉争霸时期，讲述的是西楚霸王项羽与美人虞姬之间的情感纠葛。秦朝灭亡后，项羽自立为王，统帅八千江东子弟起义抗秦，战胜了强大的秦国军队，自封为西楚霸王。然而，在楚汉争霸中失败，英雄末路时被迫自刎乌江。而他的心爱之人虞姬也投缳而死，以身殉情。\n\n### 人物情感\n项羽和虞姬之间的感情纯真而又深沉。项羽作为一代枭雄，拥有无尽的武勇和威势，但在面对爱情时却显得如此柔弱。他在战场上的英勇无敌以及战场上为他人考虑的豪迈气概，与他对待虞姬的情感形成了鲜明对比。虞姬则是一曲绝美的女声，她的美貌与才华更增添了几分凄美。她不仅为项羽而生，也为他而死，以一腔柔情见证了英雄末路时的悲凉。\n\n### 现代启示\n《霸王别姬》虽然发生在古代，但在现代同样具有深刻的启示意义。首先，它提醒我们爱情的力量是无穷的。无论是在爱情中付出多少，都能得到无尽的回报。其次，英雄主义不仅仅是战场上的英勇，更在于人性中的真善美。“生于繁华落于尘埃”的悲凉感告诉我们要珍惜当下，勇敢面对生活的挑战和困难。最后，这段历史故事也启示我们，在面对逆境时要保持坚韧不屈的精神，即便在最艰难的时刻也要坚守自己的信念。\n\n### 结语\n《霸王别姬》是中华民族悠久历史文化中的一个重要组成部分。通过这个故事，我们可以更深入地理解古代英雄与美女之间的感情纠葛以及他们所经历的悲剧命运。同时，这份爱情的美好与牺牲也让我们反思关于勇气、牺牲和个人价值的问题。在今天快节奏的社会中，这些古典文化的智慧依然能给我们带来深刻的影响和启示。\n\n---\n\n希望这篇作文能够满足你的需求。如果有其他具体的要求或者需要进一步修改，请告诉我！','2025-07-15 05:56:37'),
(1105,1,246,'user','写一篇作文','2025-07-15 05:56:28'),
(1106,1,246,'ai','好的，我们来写一篇以《霸王别姬》为背景的作文。这篇作文旨在通过描述这一段历史故事，表达英雄与美人的悲壮情感以及他们对爱情的理解。\n\n【题目】：《虞姬泪，霸王剑》\n\n【正文】\n\n在中国悠久的历史长河中，有一段凄美的传奇——“霸王别姬”。这段故事不仅在中国文学和戏剧中留下了浓墨重彩的一笔，更是成为了无数人心中的经典。它讲述的是项羽与虞姬之间深深的爱恋与无奈的结局。\n\n在那个兵荒马乱的时代，项羽凭借勇力和谋略成为一方诸侯的领袖。他在楚汉争霸中虽无敌于天下，但在心中却始终难以割舍的，是那一位绝世佳人——虞姬。虞姬不仅美丽动人，还是一位才情出众的歌女，在项羽的心中占有不可替代的地位。\n\n在垓下之战前夕，四面楚歌，项羽率领数十万大军陷入重重包围之中。夜晚，他与虞姬共度最后一次相聚的时间。月光如水，琴声悠扬，项羽不禁感慨万千。他回首往事，感叹历史的无常与爱情的脆弱。于是，便有了著名的那句“霸王别姬”的故事。\n\n项羽悲壮地说：“虞姬，生如夏花，死如秋叶。”这句话既是对虞姬一生短暂但却绚烂的生命的赞美，也是对自己命运的一种沉重诉说。面对生死存亡之际的选择，项羽选择了保护爱人的荣誉和尊严，不愿让爱人落入敌手。\n\n虞姬深情地望着项羽的眼睛，轻轻地说：“君王天下，妾身何求？愿以一舞换君安。”在琴声的伴奏下，她缓缓起舞，并用生命唱响了《霸王别姬》的传奇——那首让人既感伤又壮烈的歌。她的舞蹈如同飞鸿影里，轻盈而决绝。\n\n“虞兮虞兮奈若何，不知天亡我，项羽啊！”最后一曲结束，虞姬静静地倒下了。她以生命为代价，换来了项羽的尊严和安定。然而，这一幕也深刻地暴露了历史的真实：在这变幻莫测的社会里，英雄与美人、权力与爱情之间都充满了无奈与牺牲。\n\n尽管最终项羽在乌江边自刎谢罪天命，但他的勇气和虞姬的忠诚永远被传颂。这种悲壮的情感让人感叹：真正的爱不仅仅是相伴左右，更是在生命的重要时刻给予支持和勇气。即使在最黑暗的时刻，爱也可以成为指引前行的力量。\n\n【结语】\n\n《霸王别姬》不仅是一段历史故事，更是对真挚爱情与英雄主义的一次深刻反思。它提醒着我们，在面对抉择时，要勇敢地去追求自己的理想，并且珍惜当下拥有的一切。正是这种对人性深层次的理解和感悟，使得这段悲壮的情缘成为了传世佳话。\n\n希望这篇作文能够满足你的需求！如果有任何修改意见或者需要进一步的内容，请随时告诉我。','2025-07-15 05:56:39');
/*!40000 ALTER TABLE `tur_chat_history` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_chat_sessions`
--

DROP TABLE IF EXISTS `tur_chat_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_chat_sessions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '会话标题（通常第一句话）',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `tur_chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tur_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_chat_sessions`
--

LOCK TABLES `tur_chat_sessions` WRITE;
/*!40000 ALTER TABLE `tur_chat_sessions` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_chat_sessions` VALUES
(246,1,'你能帮我写一首歌吗？关于霸王别姬的','2025-07-15 05:55:17');
/*!40000 ALTER TABLE `tur_chat_sessions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_users`
--

DROP TABLE IF EXISTS `tur_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `phone_number` varchar(20) NOT NULL COMMENT '手机号码',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `phone_number` (`phone_number`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_users`
--

LOCK TABLES `tur_users` WRITE;
/*!40000 ALTER TABLE `tur_users` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_users` VALUES
(1,'18825130917','bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a','2025-07-10 20:19:58'),
(4,'188251309172','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-10 20:21:55'),
(5,'18825130916','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-10 20:22:28'),
(6,'18825130918','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-11 06:10:37'),
(7,'18825130999','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','2025-07-15 06:08:04'),
(8,'18825130919','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','2025-07-15 06:48:55'),
(9,'18825130920','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','2025-07-15 07:03:42');
/*!40000 ALTER TABLE `tur_users` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_verify_codes`
--

DROP TABLE IF EXISTS `tur_verify_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_verify_codes` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `phone_number` char(20) NOT NULL COMMENT '手机号',
  `code` varchar(10) NOT NULL COMMENT '验证码',
  `purpose` varchar(50) NOT NULL COMMENT '用途',
  `is_used` tinyint(1) DEFAULT 0 COMMENT '是否已使用',
  `used_at` timestamp NOT NULL COMMENT '使用时间',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_verify_codes`
--

LOCK TABLES `tur_verify_codes` WRITE;
/*!40000 ALTER TABLE `tur_verify_codes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tur_verify_codes` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-07-15  7:04:30
