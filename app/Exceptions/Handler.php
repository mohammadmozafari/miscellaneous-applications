<?php

namespace App\Exceptions;

use App\Traits\ResponseManager;
use Elasticsearch\Common\Exceptions\Missing404Exception;
use Exception;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Auth\AuthenticationException;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpKernel\Exception\HttpException;
use Symfony\Component\HttpKernel\Exception\MethodNotAllowedHttpException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

class Handler extends ExceptionHandler
{
    use ResponseManager;
    /**
     * A list of the exception types that are not reported.
     *
     * @var array
     */
    protected $dontReport = [
        //
    ];

    /**
     * A list of the inputs that are never flashed for validation exceptions.
     *
     * @var array
     */
    protected $dontFlash = [
        'password',
        'password_confirmation',
    ];

    /**
     * Report or log an exception.
     *
     * @param Exception $exception
     * @return void
     * @throws Exception
     */
    public function report(Exception $exception)
    {
        parent::report($exception);
    }

    /**
     * Render an exception into an HTTP response.
     *
     * @param Request $request
     * @param Exception $e
     * @return Response
     */
    public function render($request, Exception $e)
    {
        if (false)
        {
            dump($e);
        }
        else
        {
            if ($e instanceof ValidationException)
            {
                return $this->sendData('message', 'invalid input', 422);
            }
            if ($e instanceof ModelNotFoundException)
            {
                $modelName = strtolower(class_basename($e->getModel()));
                return $this->sendData('message', "Does not exist any {$modelName} with the specified identifier.", 404);
            }
            if ($e instanceof AuthenticationException)
            {
                return $this->sendData('message', 'unauthenticated', 401);
            }
            if ($e instanceof AuthorizationException)
            {
                return $this->sendData('message', $e->getMessage(), 403);
            }
            if ($e instanceof MethodNotAllowedHttpException)
            {
                return $this->sendData('message', "The specified method for request is invalid.", 405);
            }
            if ($e instanceof NotFoundHttpException)
            {
                return $this->sendData('message', "The specified URL cannot be found.", 404);
            }
            if ($e instanceof Missing404Exception)
            {
                return $this->sendData('message', "The specified elasticsearch node cannot be found.", 404);
            }
            if ($e instanceof HttpException)
            {
                return $this->sendData('message', $e->getMessage(), $e->getStatusCode());
            }
            if ($e instanceof QueryException)
            {
                $errorCode = $e->errorInfo[1];
                if ($errorCode == 1451)
                {
                    return $this->sendData('message', "Cannot remove this resource permanently. It is related with other resources.", 409);
                }
                return $this->sendData('message', $e->getMessage(), 403);
            }

            return $this->sendData('message', "Unexpected exception. Try later.", 500);
        }
    }
}
