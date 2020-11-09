<?php

namespace App\Jobs;

use App\Item;
use App\ItemType;
use App\Kind;
use Elasticsearch\ClientBuilder;
use Illuminate\Bus\Queueable;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;

class ElasticSave implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    private $item, $elasticsearch;

    /**
     * Create a new job instance.
     *
     * @param $item
     */
    public function __construct(Item $item)
    {
        $this->item = $item;
    }

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        $this->elasticsearch = ClientBuilder::create()->build();
        $kind = Kind::query()->findOrFail($this->item['kind_id']);
        $type = ItemType::query()->find($kind['item_type_id']);

        $this->elasticsearch->index([
            'index' => $this->item->getSearchIndex(),
            'type' => $this->item->getSearchType(),
            'id' => $this->item['id'],
            'body' => [
                'id' => $this->item['id'],
                'price' => $this->item['price'],
                'description' => $this->item['description'],
                'kind_title' => $kind['title'],
                'kind_min_price' => $kind['min_price'],
                'kind_max_price' => $kind['max_price'],
                'type_title' => $type['title'],
                'type_category' => $type['category']
            ],
        ]);
    }
}
