<?php

namespace App\Repositories;

interface ShowcaseRepository
{
    public function search($query, $num);
    public function recreate($indexName);
}
