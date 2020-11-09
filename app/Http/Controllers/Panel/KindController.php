<?php

namespace App\Http\Controllers\Panel;

use App\ItemType;
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

class KindController extends Controller
{
    use ResponseManager;

    /**
     * Display a listing of the resource.
     *
     * @return Response
     */
    public function index()
    {
        $kind = Kind::all();
        return $this->sendData('list', $kind, 200);
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
            'title' => 'required|string',
            'min_price' => 'required|numeric',
            'max_price' => 'required|numeric',
            "item_type_id" => 'required|numeric|exists:item_types,id'
        ];

        $this->validate($request, $rules);
        Kind::query()->create($request->only('title', 'min_price', 'max_price', 'item_type_id'));
        return $this->sendData('message', "Kind is queued to be created." , 201);
    }

    /**
     * Display the specified resource.
     *
     * @param Kind $kind
     * @return Response
     */
    public function show(Kind $kind)
    {
        return $this->sendData('list', [$kind], 200);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param Request $request
     * @param Kind $kind
     * @return Response
     * @throws ValidationException
     */
    public function update(Request $request, Kind $kind)
    {
        $data = $request->all();
        $rules = [
            'title' => 'string',
            'min_price' => 'numeric',
            'max_price' => 'numeric',
            "item_type_id" => 'numeric|exists:item_types,id'
        ];

        $this->validate($request, $rules);
        if (array_key_exists('title', $data))
            $kind['title'] = $data['title'];
        if (array_key_exists('min_price', $data))
            $kind['min_price'] = $data['min_price'];
        if (array_key_exists('max_price', $data))
            $kind['max_price'] = $data['max_price'];
        if (array_key_exists('item_type_id', $data))
            $kind['item_type_id'] = $data['item_type_id'];
        $kind->save();;
        return $this->sendData('message', 'Kind is queued to be updated.' , 201);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param Kind $kind
     * @return void
     * @throws Exception
     */
    public function destroy(Kind $kind)
    {
        $kind->delete();
        return $this->sendData('message', 'kind is queued to be deleted', 200);
    }
}
