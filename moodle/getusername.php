<?php
if (!file_exists('./config.php')) {
    header('Location: install.php');
    die;
}

require_once('config.php');
require_once($CFG->dirroot .'/course/lib.php');
require_once($CFG->libdir .'/filelib.php');
require_once($CFG->libdir . '/classes/encryption.php');

function getUsername() {
    $str = "sodium:KllgqOksZcOKPPh4cTpYAMMz28ZZiPPOTWgKGds5MP5Wrd5wXstWlkVAhmIF";

    $username = \core\encryption::decrypt($str);
    // print("Decrypted username: $username\n");

    if ($username === 'guest' || $username === 'nobody') {
        // backwards compatibility - we do not set these cookies any more
        $username = '';
    }
    return $username;
}

print_r(getUsername());
