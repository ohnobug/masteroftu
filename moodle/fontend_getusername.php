<?php
if (!file_exists('./config.php')) {
    header('Location: install.php');
    die;
}

require_once('config.php');
require_once($CFG->dirroot .'/course/lib.php');
require_once($CFG->libdir .'/filelib.php');
require_once($CFG->libdir . '/classes/encryption.php');


class SimpleCrypto {

    // 加密方法
    private static $cipher = "aes-256-cbc";

    /**
     * 生成一个安全的随机加密密钥。
     *
     * @param string $bytes 密钥的字节长度，推荐 32 字节 (256 位)。
     * @return string 经过 base64 编码的密钥。
     * @throws Exception 如果无法生成随机字节。
     */
    public static function generateKey(int $bytes = 32): string {
        // 使用 openssl_random_pseudo_bytes 生成加密安全的随机字节
        // OPENSSL_RAW_DATA 选项返回原始字节串
        $key = openssl_random_pseudo_bytes($bytes, $crypto_strong);
        if (!$crypto_strong) {
            throw new Exception("无法生成加密安全的随机字节。");
        }
        // 返回 base64 编码的密钥，方便存储和传输
        return base64_encode($key);
    }

    /**
    * 生成一个安全的随机初始化向量 (IV)。
    * IV 的长度必须与加密算法的块大小一致。
    * 对于 AES-256-CBC，块大小是 16 字节。
    *
    * @return string 经过 base64 编码的 IV。
    * @throws Exception 如果无法生成随机字节。
    */
    private static function generateIV(): string {
        $iv_len = openssl_cipher_iv_length(self::$cipher);
        if ($iv_len === false) {
            throw new Exception("无法获取cipher '{$this->cipher}' 的IV长度。");
        }
        $iv = openssl_random_pseudo_bytes($iv_len, $crypto_strong);
        if (!$crypto_strong) {
            throw new Exception("无法生成加密安全的随机字节作为IV。");
        }
        return base64_encode($iv);
    }

    /**
     * 加密数据。
     *
     * @param string $data 要加密的数据。
     * @param string $key 用于加密的密钥 (base64 编码)。
     * @return string|false 加密后的数据 (base64 编码)，失败则返回 false。
     * @throws Exception 如果加密过程出错。
     */
    public static function encrypt(string $data, string $key): string|false {
        // 1. 解码密钥
        $decodedKey = base64_decode($key);
        if ($decodedKey === false) {
            throw new Exception("无效的密钥格式 (base64 编码错误)。");
        }

        // 2. 生成随机 IV
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length(self::$cipher), $crypto_strong);
        if (!$crypto_strong) {
            throw new Exception("无法生成加密安全的随机字节作为IV。");
        }
        $iv_base64 = base64_encode($iv); // 将 IV 也 base64 编码，以便与密文一起存储

        // 3. 执行加密
        // OPENSSL_RAW_DATA: 返回原始的二进制密文
        // OPENSSL_ZERO_PADDING: 如果不需要填充（例如数据本身就是块大小的倍数），可以指定此选项
        $encryptedData = openssl_encrypt($data, self::$cipher, $decodedKey, OPENSSL_RAW_DATA, $iv);

        if ($encryptedData === false) {
            throw new Exception("加密失败: " . openssl_error_string());
        }

        // 4. 返回一个包含 IV 和密文的组合字符串
        // 通常是 IV + 密文，以便解密时能同时获取 IV
        // 使用 base64 编码方便存储和传输
        return base64_encode($iv . $encryptedData);
    }

    /**
     * 解密数据。
     *
     * @param string $encryptedData 加密后的数据 (base64 编码，包含 IV 和密文)。
     * @param string $key 用于解密的密钥 (base64 编码)。
     * @return string|false 解密后的原始数据，失败则返回 false。
     * @throws Exception 如果解密过程出错。
     */
    public static function decrypt(string $encryptedData, string $key): string|false {
        // 1. 解码密钥
        $decodedKey = base64_decode($key);
        if ($decodedKey === false) {
            throw new Exception("无效的密钥格式 (base64 编码错误)。");
        }

        // 2. 解码输入的加密数据 (它包含 IV 和密文)
        $decodedEncryptedData = base64_decode($encryptedData);
        if ($decodedEncryptedData === false) {
            throw new Exception("无效的加密数据格式 (base64 编码错误)。");
        }

        // 3. 计算 IV 的长度
        $iv_len = openssl_cipher_iv_length(self::$cipher);
        if ($iv_len === false) {
            throw new Exception("无法获取cipher '{$this->cipher}' 的IV长度。");
        }

        // 4. 提取 IV 和密文
        // 密文是从 decodedEncryptedData 中截取 IV_LEN 之后的剩余部分
        $iv = substr($decodedEncryptedData, 0, $iv_len);
        $encryptedText = substr($decodedEncryptedData, $iv_len);

        // 5. 执行解密
        // OPENSSL_RAW_DATA: 密文是原始二进制格式
        $decryptedData = openssl_decrypt($encryptedText, self::$cipher, $decodedKey, OPENSSL_RAW_DATA, $iv);

        if ($decryptedData === false) {
            throw new Exception("解密失败: " . openssl_error_string());
        }

        return $decryptedData;
    }
}

// try {
//     $secretKey = SimpleCrypto::generateKey(); // 生成一个 32 字节 (256位) 的密钥
//     echo "生成的密钥 (base64): " . $secretKey . "\n\n";

//     $originalData = "这是一个需要被加密的秘密信息，包含中文和特殊字符：你好世界！@#$%^&*()";
//     echo "原始数据: " . $originalData . "\n";

//     // 加密数据
//     $encrypted = SimpleCrypto::encrypt($originalData, $secretKey);
//     if ($encrypted) {
//         echo "加密后的数据 (base64): " . $encrypted . "\n";

//         // 解密数据
//         $decrypted = SimpleCrypto::decrypt($encrypted, $secretKey);
//         if ($decrypted !== false) {
//             echo "解密后的数据: " . $decrypted . "\n";

//             // 验证解密是否正确
//             if ($originalData === $decrypted) {
//                 echo "✅ 加密和解密过程成功！数据一致。\n";
//             } else {
//                 echo "❌ 加密和解密过程成功，但数据不一致！\n";
//             }
//         } else {
//             echo "❌ 解密失败。\n";
//         }
//     } else {
//         echo "❌ 加密失败。\n";
//     }

// } catch (Exception $e) {
//     echo "发生错误: " . $e->getMessage() . "\n";
// }


function getUsername() {
    $str = $_COOKIE['MOODLEID1_'];

    if (empty($str)) {
        return '';
    }

    $username = \core\encryption::decrypt($str);

    if ($username === 'guest' || $username === 'nobody') {
        $username = '';
    }
    return $username;
}


// 定义允许的Referer来源
$allowed_referers = [
    'http://localhost:5173',
    'https://turcar.net.cn',
    'https://learn.turcar.net.cn',
];

// 获取HTTP_REFERER头
// $http_referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : '';
$http_referer = $_SERVER['HTTP_ORIGIN'];

// 检查Referer是否为空或者不符合要求
if (!empty($http_referer)) {
    // 简单地匹配完整URL，更健壮的实现可能需要解析URL
    foreach ($allowed_referers as $allowed_referer) {
        // 使用strpos来检查Referer是否以允许的来源开头
        // 注意：这里使用strpos进行简单的匹配，对于更复杂的验证（如查询参数），
        // 可能需要使用parse_url进行URL解析和更精细的比较。
        if (strpos($http_referer, $allowed_referer) === 0) {
            header("Access-Control-Allow-Origin: " . $allowed_referer);
            // 如果找到匹配项，可以立即停止循环并返回
            // 注意：如果你允许多个来源，并且希望浏览器知道所有允许的来源，
            // 你需要在这里收集所有匹配的来源，然后合并成一个逗号分隔的字符串，
            // 例如：header("Access-Control-Allow-Origin: https://source1.com, https://source2.com");
            // 但是，W3C规范建议Access-Control-Allow-Origin只能有一个值。
            // 最常见且安全的做法是将其设置为允许的某个具体来源。
            // 如果你的前端只需要知道"是允许的"，那么设置第一个匹配的即可。
            // 如果你需要精确控制，可以根据前端请求的Origin来匹配，如下面的进阶用法。
            break; // 找到匹配的Referer后退出循环
        }
    }
}
header('Access-Control-Allow-Credentials: true');




$userinfo = $_SESSION['USER'];
$username = $userinfo->username ?? "";

// // $username = getUsername();
if (empty($username)) {
    header('Content-Type: application/json');
    echo json_encode(['code' => 404, 'message' => '未找到用户名']);
    exit;
} else {    
    // $secretKey = SimpleCrypto::generateKey(); // 生成一个 32 字节 (256位) 的密钥
    // echo "生成的密钥 (base64): " . $secretKey . "\n\n";
    // $secretKey = '1ocxv0tgU07NaKmneiQUbAR2RJrbrJnhAgNW1cYufjI=';
    // $originalData = trim($username);

    // 加密数据
    // $encrypted = SimpleCrypto::encrypt($originalData, $secretKey);
    header('Content-Type: application/json');
    echo json_encode(
        ['code' => 200, 'message' => '', 'data' => ['userinfo' => $userinfo]]
    );
}

