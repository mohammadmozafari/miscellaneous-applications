<?php

use App\Item;
use App\ItemType;
use App\Kind;
use App\Repositories\ShowcaseRepository;
use App\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @param ShowcaseRepository $repo
     * @return void
     */
    public function run(ShowcaseRepository $repo)
    {
        DB::statement('SET FOREIGN_KEY_CHECKS = 0');

        User::query()->truncate();
        Item::query()->truncate();
        Kind::query()->truncate();
        ItemType::query()->truncate();

        $repo->recreate('items');

        $items = 50;
        $kinds = 20;
        $itemTypes = 10;

//        User::flushEventListeners();
//        Item::flushEventListeners();
//        Kind::flushEventListeners();
//        ItemType::flushEventListeners();

        factory(ItemType::class, $itemTypes)->create();
        factory(Kind::class, $kinds)->create();
        factory(Item::class, $items)->create();
    }
}
