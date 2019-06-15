<?php


namespace App\Repositories;

use App\Item;
use Elasticsearch\ClientBuilder;

class ElasticsearchShowcaseRepository implements ShowcaseRepository
{
    private $elastic;

    public function __construct()
    {
        $this->elastic = ClientBuilder::create()->build();
    }

    public function search($query, $num)
    {
        $instance = new Item;
        $match = array();

        // range ( price - 10, price + 10)
        if (array_key_exists('price', $query))
            array_push($match, array('range' => array('price' =>
                array('gte' => $query['price'] - 10, 'lte' => $query['price'] + 10))));

        // must match
        if (array_key_exists('description', $query))
            array_push($match, array('match' => array('description' => $query['description'])));
        if (array_key_exists('kindTitle', $query))
            array_push($match, array('match' => array('kind_title' => $query['kindTitle'])));
        if (array_key_exists('typeTitle', $query))
            array_push($match, array('match' => array('type_title' => $query['typeTitle'])));
        if (array_key_exists('category', $query))
            array_push($match, array('match' => array('type_category' => $query['category'])));

        $elasticQuery = [
            'index' => 'shit',
            'type' => $instance->getSearchType(),
            'body' => [
                'query' => [
                    "bool" => [
                        "must" => $match
                        ],
                    ],
                ],
                'from' => ($num - 1) * 5,
                'size' => 5
            ];


        $results = $this->elastic->search($elasticQuery);
        $results = $this->buildCollection($results, $num);

        return $results;
    }

    public function recreate($indexName)
    {
        if ($this->elastic->indices()->exists(['index' => $indexName]))
            $this->elastic->indices()->delete(['index' => $indexName]);
        $this->elastic->indices()->create(['index' => $indexName]);
    }

    private function buildCollection(array $items, $num)
    {
        /**
         * The data comes in a structure like this:
         *
         * [
         *      'hits' => [
         *          'hits' => [
         *              [ '_source' => 1 ],
         *              [ '_source' => 2 ],
         *          ]
         *      ]
         * ]
         *
         * And we only care about the _source of the documents.
         */
        $total = $items['hits']['total'];
        $sources = array_pluck($items['hits']['hits'], ['_source']) ?: [];
        $sources['total'] = $total;
        $sources['range'] = 'results from ' . ($num - 1) * 5 . ' to ' . ($num * 5 - 1);
        return $sources;
    }
}
