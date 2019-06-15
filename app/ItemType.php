<?php

namespace App;

use App\Traits\Searchable;
use Illuminate\Database\Eloquent\Model;

class ItemType extends Model
{
    protected $fillable = [
        'title',
        'category'
    ];

//    protected $mappingProperties = array(
//        'title' => [
//            'type' => 'text',
//            'analyzer' => 'standard'
//        ],
//        'description' => [
//            'type' => 'text',
//            'analyzer' => 'standard'
//        ],
//    );

    public function kinds()
    {
        return $this->hasMany(Kind::class);
    }
}
