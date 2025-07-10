/*
 Navicat Premium Dump SQL

 Source Server         : local2
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : localhost:3308
 Source Schema         : tur

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 10/07/2025 21:25:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tur_chat_history
-- ----------------------------
DROP TABLE IF EXISTS `tur_chat_history`;
CREATE TABLE `tur_chat_history`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `chat_session_id` bigint(20) NOT NULL,
  `sender` enum('ai','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `text` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `chat_session_id`(`chat_session_id` ASC) USING BTREE,
  CONSTRAINT `tur_chat_history_ibfk_1` FOREIGN KEY (`chat_session_id`) REFERENCES `tur_chat_sessions` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 802 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tur_chat_history
-- ----------------------------

-- ----------------------------
-- Table structure for tur_chat_sessions
-- ----------------------------
DROP TABLE IF EXISTS `tur_chat_sessions`;
CREATE TABLE `tur_chat_sessions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 118 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tur_chat_sessions
-- ----------------------------

-- ----------------------------
-- Table structure for tur_sms_logs
-- ----------------------------
DROP TABLE IF EXISTS `tur_sms_logs`;
CREATE TABLE `tur_sms_logs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tur_sms_logs
-- ----------------------------

-- ----------------------------
-- Table structure for tur_users
-- ----------------------------
DROP TABLE IF EXISTS `tur_users`;
CREATE TABLE `tur_users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone_number`(`phone_number` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tur_users
-- ----------------------------
INSERT INTO `tur_users` VALUES (1, '18825130917', '71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500', '2025-07-10 20:19:58');
INSERT INTO `tur_users` VALUES (4, '188251309172', '71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500', '2025-07-10 20:21:55');
INSERT INTO `tur_users` VALUES (5, '18825130916', '71b9b90bafe13be75924c7b06733f90919b2226f663935322b3882dfb8f4e500', '2025-07-10 20:22:28');

-- ----------------------------
-- Table structure for tur_verification_codes
-- ----------------------------
DROP TABLE IF EXISTS `tur_verification_codes`;
CREATE TABLE `tur_verification_codes`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `purpose` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_used` tinyint(1) NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tur_verification_codes
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
