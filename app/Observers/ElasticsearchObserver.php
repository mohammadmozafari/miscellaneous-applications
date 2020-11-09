<?php


namespace App\Observers;

use App\Item;
use App\ItemType;
use App\Jobs\ElasticSave;
use App\Kind;
use Elasticsearch\ClientBuilder;

class ElasticsearchObserver
{
    private $elasticsearch;

    public function __construct()
    {
        $this->elasticsearch = ClientBuilder::create()->build();
    }

    public function saved(Item $item)
    {
        ElasticSave::dispatch($item);
    }

    public function deleted(Item $item)
    {
        $this->elasticsearch->delete([
            'index' => $item->getSearchIndex(),
            'type' => $item->getSearchType(),
            'id' => $item['id'],
        ]);
    }
}
