package com.example.coroutinetest01.fragment


import android.os.Bundle
import android.support.v4.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import kotlinx.android.synthetic.main.fragment_button.*
import kotlinx.coroutines.*
import com.example.coroutinetest01.R
import java.util.*
import java.util.concurrent.TimeUnit

class ExceptionFragment : Fragment() {

    private val uiDispatcher: CoroutineDispatcher = Dispatchers.Main
    private val dataProvider = DataProvider()
    private lateinit var job: Job
    companion object {
        const val TAG = "ExceptionFragment"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        job = Job()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_button, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        button.setOnClickListener { loadData() }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        job.cancel()
    }

    private fun loadData() = GlobalScope.launch(uiDispatcher + job) {
        showLoading()

        /* launch는 error가 발생하여도 리턴되지않습니다.
           - 때문에 ErrorHandler를 사용하거나 아래와같이 try catch문을 이용합니다.
        */
        try {
            val result = dataProvider.loadData()
            showText(result)
        } catch (e: IllegalArgumentException) {
            showText(e.message ?: "")
        }

        hideLoading()
    }

    private fun showLoading() {
        progressBar.visibility = View.VISIBLE
    }

    private fun hideLoading() {
        progressBar.visibility = View.GONE
    }

    private fun showText(data: String) {
        textView.text = data
    }

    class DataProvider(private val dispatcher: CoroutineDispatcher = Dispatchers.IO) {

        suspend fun loadData(): String = withContext(dispatcher) {
            delay(TimeUnit.SECONDS.toMillis(2)) // imitate long running operation
            mayThrowException()
            "Data is available: ${Random().nextInt()}"
        }

        /* Exception 처리 */
        private fun mayThrowException() {
            if (Random().nextBoolean()) {
                throw IllegalArgumentException("Ooops exception occurred")
            }
        }
    }

}