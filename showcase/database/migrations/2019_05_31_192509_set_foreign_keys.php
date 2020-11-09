<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class SetForeignKeys extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('items', function (Blueprint $table) {
            $table->foreign('kind_id')->references('id')->on('kinds');
        });
        Schema::table('kinds', function (Blueprint $table) {
            $table->foreign('item_type_id')->references('id')->on('item_types');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('items', function (Blueprint $table) {
            $table->dropForeign('items_kind_id_foreign');
        });
        Schema::table('kinds', function (Blueprint $table) {
            $table->dropForeign('kinds_item_type_id_foreign');
        });
    }
}
