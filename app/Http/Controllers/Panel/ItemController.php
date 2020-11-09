<?php

namespace App\Http\Controllers\Panel;

use App\Item;
use App\Jobs\Create;
use App\Jobs\Delete;
use App\Jobs\Update;
use App\Kind;
use App\Traits\ResponseManager;
use Exception;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Http\Response;
use Illuminate\Validation\ValidationException;

class ItemController extends Controller
{
    use ResponseManager;

    /**
     * Display a listing of the resource.
     *
     * @return Response
     */
    public function index()
    {
        $items = Item::all();
        return $this->sendData('list', $items, 200);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param Request $request
     * @return Response
     * @throws ValidationException
     */
    public function store(Request $request)
    {
        $rules = [
            'kind_id' => 'required|numeric|exists:kinds,id',
        ];
        $this->validate($request, $rules);
        $kind = Kind::query()->find($request['kind_id']);
        $minp = $kind['min_price'];
        $maxp = $kind['max_price'];
        $rules = [
            'price' => "required|numeric|between:{$minp},{$maxp}",
            'description' => 'required|string',
        ];
        $this->validate($request, $rules);

        Item::query()->create($request->only('price', 'description', 'kind_id'));
        return $this->sendData('message', 'Item is created.', 201);
    }

    /**
     * Display the specified resource.
     *
     * @param Item $item
     * @return Response
     */
    public function show(Item $item)
    {
        return $this->sendData('list', [$item], 200);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param Request $request
     * @param Item $item
     * @return Response
     * @throws ValidationException
     */
    public function update(Request $request, Item $item)
    {
        $data = $request->all();
        $rules = [
            'kind_id' => 'numeric|exists:kinds,id',
        ];
        $this->validate($request, $rules);
        if (array_key_exists('kind_id', $data))
            $kind = Kind::query()->find($request['kind_id']);
        else
            $kind = $item['kind'];
        $minp = $kind['min_price'];
        $maxp = $kind['max_price'];
        $rules = [
            'price' => "numeric|between:{$minp},{$maxp}",
            'description' => 'string',
        ];
        $this->validate($request, $rules);
        if (array_key_exists('price', $data))
            $item['price'] = $data['price'];
        if (array_key_exists('description', $data))
            $item['description'] = $data['description'];
        if (array_key_exists('kind_id', $data))
            $item['kind_id'] = $data['kind_id'];
        $item->save();
        return $this->sendData('message', 'Item is updated.', 201);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param Item $item
     * @return void
     * @throws Exception
     */
    public function destroy(Item $item)
    {
        $item->delete();
        return $this->sendData('message', 'item is deleted', 200);
    }
}
