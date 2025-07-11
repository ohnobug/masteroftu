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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `chat_session_id` bigint(20) NOT NULL,
  `sender` enum('ai','user') DEFAULT NULL,
  `text` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `chat_session_id` (`chat_session_id`) USING BTREE,
  CONSTRAINT `tur_chat_history_ibfk_1` FOREIGN KEY (`chat_session_id`) REFERENCES `tur_chat_sessions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=820 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_chat_history`
--

LOCK TABLES `tur_chat_history` WRITE;
/*!40000 ALTER TABLE `tur_chat_history` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_chat_history` VALUES
(812,1,122,'user','可以写篇小说吗？','2025-07-10 22:02:43'),
(813,1,122,'ai','当然，可以帮您构思并创作一篇短篇小说。下面为您讲述一个关于梦想与抉择的温馨故事：\n\n---\n\n### 题目：梦之桥\n\n小镇上的天气总是那么宜人，仿佛时间在这里静止了一般。在小镇的一隅，住着一个叫林晨的年轻人，他有着一双渴望探求未知的眼睛和一颗对音乐深爱的心。\n\n林晨出生在一个音乐世家，从小就受到了长辈们的悉心教导。但他内心深处却藏着另一个秘密——梦想成为一位旅行家，在世界上的每一个角落留下自己的足迹。每当看到远方的星辰时，他就会默默许愿，希望能与这个世界更加亲近而不是只能通过音符来感受它。\n\n直到有一天，林晨得到了一张特殊的邀请函，邀请他参加在海边举行的一个国际音乐节。虽然机会难得，但考虑到这可能会成为自己离梦想更进一步的关键一步，他在内心反复权衡着选择：旅行家的梦想和对音乐的热爱究竟哪一个更重要？\n\n正当林晨纠结不已之时，他的爷爷从家中走了出来。“你是个勇敢的孩子，”他这样说道，“但不要忘记真正的勇气是要知道自己最珍贵的东西是什么并且勇于为之奋斗。”\n\n这句话仿佛为林晨指明了方向。他理解到，在这段短暂的生活旅程中，有太多值得珍惜的瞬间——与家人朋友共度的美好时光、追求音乐理想的机会以及未知路上等待探索的可能性。\n\n于是，林晨决定带上爷爷赠送的一张珍贵吉他专辑和一把爷爷亲手制作的小提琴踏上了前往海边的旅程。在旅途中，他还结识了许多志同道合的朋友，也听到了更多不同的音乐故事，这些经历进一步丰富了他的心灵世界。\n\n最终，在那个充满浪漫与梦想的地方，林晨不仅实现了自我价值，还找到了属于自己的那份平衡——在探索世界的脚步中不忘记用音符编织出心中那座通往美好之处的梦之桥。而这段旅程也成为了他生命中最宝贵的回忆之一。\n\n---\n\n这是一个简短的故事，希望您喜欢！如果您有特定的主题或情节设定也可以告知我，我可以根据不同要求来创作。','2025-07-10 22:02:52'),
(814,1,122,'user','可以帮我写个python教程吗？','2025-07-10 22:03:06'),
(815,1,122,'ai','当然可以！下面是一个面向初学者的Python编程教程，涵盖基础知识和一些实用示例。\n\n### Python 入门教程：从零开始学 Python\n\n#### 目标读者\n- 初级至中级开发者\n- 对编程感兴趣并希望学习 Python 的人群\n\n#### 必备工具\n1. 一个文本编辑器或 IDE（例如 VSCode、PyCharm）\n2. 安装 Python (建议使用最新稳定版本)\n\n#### 第一步：安装 Python\n首先，请访问 [Python 官方网站](https://www.python.org/downloads/) 下载并安装适合您操作系统的最新版 Python。\n\n在命令行中输入 `python --version` （在 Windows 中是 `py --version`）来确认是否已经正确安装。\n\n#### 第二步：创建第一个 Python 程序\n打开您的文本编辑器或 IDE，新建一个文件，并将文件扩展名更改为 `.py`。比如命名为 `hello_world.py`。\n\n输入以下代码：\n```python\n# hello_world.py\n\nprint(\"Hello, World!\")\n```\n\n保存并运行此程序（在命令行中导航到该文件所在目录并在其中输入 `python hello_world.py`）。您会看到输出：`Hello, World!`。\n\n#### 第三步：深入了解 Python 语法\n##### 注释\n- 单行注释使用 `#`\n```python\n# 这是一条单行注释\n```\n- 多行注释可以使用三个连续的引号（单或双）\n```python\n\'\'\'\n这是一个多行注释的例子。\n可以跨越多行，功能与多行字符串相同。\n\'\'\'\n```\n\n##### 变量和数据类型\nPython 是动态类型的语言，您无需提前声明变量的类型。以下是一些基本的数据类型：\n- 整数 (`int`)\n- 浮点数 (`float`)\n- 字符串 (`str`)\n- 布尔值 (`bool`)\n\n```python\nage = 25         # 整型：int\nheight = 180.5   # 浮点型：float\nname = \"Alice\"   # 字符串：str\nis_student = True  # 布尔型：bool\n\nprint(age, height, name, is_student)\n```\n\n##### 控制流语句\n- 条件语句 `if` 和 `else`\n```python\nage = int(input(\"请输入您的年龄: \"))\nif age < 18:\n    print(\"您还是未成年人。\")\nelse:\n    print(\"您已经成年了。\")\n```\n\n- 循环语句 `for` 和 `while`\n```python\n# 遍历一个范围\nfor i in range(5):\n    print(i)\n\n# 使用 while 循环\ncount = 0\nwhile count < 3:\n    print(\"计数: \", count)\n    count += 1\n```\n\n##### 函数定义与调用\n```python\ndef greet(name, age):\n    \"\"\" 这是一个打招呼的函数 \"\"\"\n    return f\"你好，{name}。你今年{age}岁了！\"\n\nprint(greet(\"Tom\", 30))\n```\n\n#### 第四步：使用 Python 标准库和第三方库\nPython 提供了许多内置库来方便开发，例如 `math`、`datetime` 等。\n\n示例：\n```python\nimport math\n\n# 使用数学库中的函数\nprint(math.sqrt(16))  # 输出 4.0\n\nfrom datetime import datetime\n\ncurrent_date = datetime.now()\nprint(\"当前日期和时间:\", current_date)\n```\n\n如果您想要安装第三方库，可以使用 `pip`。例如：\n```sh\npip install requests\n```\n然后在程序中导入并使用它。\n```python\nimport requests\n\nresponse = requests.get(\"https://api.github.com\")\nprint(response.status_code)  # 输出 HTTP 状态码\n```\n\n#### 第五步：进阶学习资源\n- [官方文档](https://docs.python.org/3/)\n- [Real Python](https://realpython.com/)\n- 教程视频如 [YouTube PyBites 学习频道](https://www.youtube.com/c/pybites)\n\n以上内容涵盖了一些基本的 Python 语法和实用示例。希望对您的学习有所帮助！如果您有任何问题或需要进一步的帮助，请随时提问。','2025-07-10 22:03:18'),
(816,1,123,'user','hello','2025-07-10 22:04:04'),
(817,1,123,'ai','Hello! How can I assist you today? Feel free to ask me questions or let me know if you need help with anything specifically.','2025-07-10 22:04:05'),
(818,1,123,'user','可以写篇作文吗？','2025-07-10 22:04:23'),
(819,1,123,'ai','当然可以！请告诉我你希望这篇作文的主题是什么？比如是关于自然、科技、教育、友情等，还是有特定的要求或要求的字数呢？这样我可以更好地帮助你。如果你没特别的想法，我来给你一个主题：《科技进步与未来生活》。\n\n---\n\n标题：《科技进步与未来生活》\n\n在这个飞速发展的时代里，“科技”一词已经成为我们生活中不可或缺的一部分。它像一股不可阻挡的力量，推动着人类社会不断向前发展。今天，我想探讨一下科技进步对我们的生活方式将产生何种影响，并展望一个美好的未来。\n\n自从工业革命以来，科学技术的进步就一直在塑造着世界。从最初的火车、电话到现在的互联网、电动汽车，每一次技术革新都极大地提高了人们的生活质量。例如，智能手机的发明不仅仅是通讯工具的革新；它改变了人们的购物方式、学习模式乃至整个社会的信息传播速度。这说明，科技进步并非孤立于我们的生活中，而是深深融入了每一个人的日常。\n\n未来，科技的进步将如何重塑人类生活呢？或许可以预见的是，人工智能和机器人技术将进一步普及应用，从而大大提高生产效率与生活质量。想象一下，未来的家庭中，不仅有智能家电帮助我们更好地管理家务，还有陪伴型机器人能够成为我们的朋友；在医疗领域，精准医疗和远程医疗服务的发展让患者无需长途跋涉就能享受到优质治疗……\n\n此外，在教育方面，虚拟现实技术将为学习者提供一个沉浸式的环境，使得知识的获取变得生动而真实。人们不再局限于书本中的知识，而是能够通过视觉、触觉等多重感官体验来深入了解各种现象和理论。\n\n不过值得注意的是，科技进步带来便利的同时也伴随着挑战。如何平衡个人隐私与安全？哪些职业将受到人工智能的影响而被淘汰？这些问题都是我们在享受科技带来的好处时必须考虑清楚的。\n\n总的来说，科技进步无疑是推动社会前进的关键力量之一。面对新的机遇与挑战，人类需要保持开放的心态和前瞻性思维去拥抱它，并积极寻求解决方案来促进和谐发展。只有这样，我们才能共同创造一个更加美好的未来生活。\n\n---\n\n这篇作文围绕“科技进步与未来生活”的主题展开讨论，涵盖科技进步的影响、未来可能的发展方向以及面临的挑战。希望对你有帮助！如果有其他需求或想要调整的方向，请告诉我。','2025-07-10 22:04:29');
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_chat_sessions`
--

LOCK TABLES `tur_chat_sessions` WRITE;
/*!40000 ALTER TABLE `tur_chat_sessions` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_chat_sessions` VALUES
(122,1,'可以写篇小说吗？','2025-07-10 22:02:43'),
(123,1,'hello','2025-07-10 22:04:04');
/*!40000 ALTER TABLE `tur_chat_sessions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_sms_logs`
--

DROP TABLE IF EXISTS `tur_sms_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_sms_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `status` varchar(20) NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_sms_logs`
--

LOCK TABLES `tur_sms_logs` WRITE;
/*!40000 ALTER TABLE `tur_sms_logs` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tur_sms_logs` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_users`
--

DROP TABLE IF EXISTS `tur_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `phone_number` (`phone_number`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_users`
--

LOCK TABLES `tur_users` WRITE;
/*!40000 ALTER TABLE `tur_users` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tur_users` VALUES
(1,'18825130917','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-10 20:19:58'),
(4,'188251309172','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-10 20:21:55'),
(5,'18825130916','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-10 20:22:28'),
(6,'18825130918','71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500','2025-07-11 06:10:37');
/*!40000 ALTER TABLE `tur_users` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tur_verification_codes`
--

DROP TABLE IF EXISTS `tur_verification_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tur_verification_codes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) NOT NULL,
  `code` varchar(10) NOT NULL,
  `purpose` varchar(50) NOT NULL,
  `is_used` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tur_verification_codes`
--

LOCK TABLES `tur_verification_codes` WRITE;
/*!40000 ALTER TABLE `tur_verification_codes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tur_verification_codes` ENABLE KEYS */;
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

-- Dump completed on 2025-07-11  7:13:49
