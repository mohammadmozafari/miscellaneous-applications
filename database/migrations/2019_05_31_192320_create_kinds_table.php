<?php

use App\Item;
use App\ItemType;
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateKindsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('kinds', function (Blueprint $table) {
            $table->bigIncrements('id') ;
            $table->string('title');
            $table->float('min_price');
            $table->float('max_price');
            $table->bigInteger('item_type_id')->unsigned();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('kinds');
    }
}
