<?php

namespace App\Jobs;

use App\Item;
use App\ItemType;
use App\Kind;
use Illuminate\Bus\Queueable;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;

class Update implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public const ITEM = 1, TYPE = 2, KIND = 3;
    private $mode, $data, $target;

    /**
     * Create a new job instance.
     *
     * @param $mode
     * @param $data
     * @param $target
     */
    public function __construct($mode, $data, $target)
    {
        $this->mode = $mode;
        $this->data = $data;
        $this->target = $target;
    }

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        if ($this->mode == self::ITEM)
        {
            if (array_key_exists('price', $this->data))
                $this->target['price'] = $this->data['price'];
            if (array_key_exists('description', $this->data))
                $this->target['description'] = $this->data['description'];
            if (array_key_exists('kind_id', $this->data))
                $this->target['kind_id'] = $this->data['kind_id'];
            $this->target->save();
        }
        else if ($this->mode == self::TYPE)
        {
            if (array_key_exists('title', $this->data))
                $this->target['title'] = $this->data['title'];
            if (array_key_exists('category', $this->data))
                $this->target['category'] = $this->data['category'];
            $this->target->save();
        }
        else if ($this->mode == self::KIND)
        {
            if (array_key_exists('title', $this->data))
                $this->target['title'] = $this->data['title'];
            if (array_key_exists('min_price', $this->data))
                $this->target['min_price'] = $this->data['min_price'];
            if (array_key_exists('max_price', $this->data))
                $this->target['max_price'] = $this->data['max_price'];
            if (array_key_exists('item_type_id', $this->data))
                $this->target['item_type_id'] = $this->data['item_type_id'];
            $this->target ->save();
        }
    }
}
