<?php

namespace App;

use App\Traits\Searchable;
use Illuminate\Database\Eloquent\Model;

class Kind extends Model
{
    protected $fillable = [
        'title',
        'min_price',
        'max_price',
        'item_type_id'
    ];

//    protected $mappingProperties = array(
//        'title' => [
//            'type' => 'text',
//            'analyzer' => 'standard'
//        ],
//        'min_price' => [
//            'type' => 'float',
//            'analyzer' => 'standard'
//        ],
//        'max_price' => [
//            'type' => 'float',
//            'analyzer' => 'standard'
//        ],
//        'item_type_id' => [
//            'type' => 'long',
//            'analyzer' => 'standard'
//        ],
//    );

    public function items()
    {
        return $this->hasMany(Item::class);
    }

    public function itemType()
    {
        return $this->belongsTo(ItemType::class);
    }
}
