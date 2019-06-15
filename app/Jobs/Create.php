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

class Create implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public const ITEM = 1, TYPE = 2, KIND = 3;
    private $mode, $data;

    /**
     * Create a new job instance.
     *
     * @param $mode
     * @param $data
     */
    public function __construct($mode, $data)
    {
        $this->mode = $mode;
        $this->data = $data;
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
            Item::query()->create($this->data);
        }
        else if ($this->mode == self::TYPE)
        {
            ItemType::query()->create($this->data);
        }
        else if ($this->mode == self::KIND)
        {
            Kind::query()->create($this->data);
        }
    }
}
