<?php


namespace App\Repositories;

use App\Traits\ResponseManager;
use Illuminate\Support\Facades\DB;

class EloquentShowcaseRepository implements ShowcaseRepository
{
    public function search($query, $num)
    {
        $sqlQuery =
            "SELECT items.id, items.price, items.description, kinds.title AS kindTitle, item_types.title AS typeTitle, item_types.category
             FROM items INNER JOIN kinds ON items.kind_id=kinds.id INNER JOIN item_types ON kinds.item_type_id=item_types.id";

        if (array_key_exists('price', $query))
            $sqlQuery = $sqlQuery . " WHERE items.price={$query['price']}";
        if (array_key_exists('description', $query))
            $sqlQuery = $sqlQuery . " WHERE items.description like '%{$query['description']}%'";
        if (array_key_exists('kindTitle', $query))
            $sqlQuery = $sqlQuery . " WHERE kinds.title='{$query['kindTitle']}'";
        if (array_key_exists('typeTitle', $query))
            $sqlQuery = $sqlQuery . " WHERE item_types.title='{$query['typeTitle']}'";
        if (array_key_exists('category', $query))
            $sqlQuery = $sqlQuery . " WHERE item_types.category='{$query['category']}'";

        $results = DB::select($sqlQuery);

        return $results;
    }

    public function recreate($indexName)
    {
        // TODO: Implement recreate() method.
    }
}
