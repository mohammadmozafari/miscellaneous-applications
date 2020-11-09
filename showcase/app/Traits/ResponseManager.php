<?php

namespace App\Traits;

trait ResponseManager
{
    public function sendData($type, $data, $statusCode)
    {
        return response()->json(['type' => $type, 'data' => $data, 'statusCode' => $statusCode]);
    }
}
