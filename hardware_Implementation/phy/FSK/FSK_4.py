#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: 4FSK
# Author: tobias
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
import numpy
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class FSK_4(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "4FSK", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("4FSK")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "FSK_4")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.spec_eff = spec_eff = 0.3
        self.bw = bw = 25e3
        self.fsk = fsk = 4
        self.TH = TH = bw*spec_eff
        self.vco_sens = vco_sens = 2*math.pi*TH/(fsk-1)
        self.variable_0_0 = variable_0_0 = 0
        self.transition_bw = transition_bw = 2e3
        self.samp_rate = samp_rate = 200e3
        self.interp = interp = 50

        ##################################################
        # Blocks
        ##################################################

        self._interp_range = qtgui.Range(1, 1000, 10, 50, 200)
        self._interp_win = qtgui.RangeWidget(self._interp_range, self.set_interp, "'interp'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._interp_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Input/Output check", #name
            4, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Orignial Signal', 'Quad demod out', 'Recieved "byte"', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            'Time sink', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            samp_rate, #bw
            "Demod freq", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            4096, #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            samp_rate, #bw
            "VCO", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0_0_0 = filter.freq_xlating_fir_filter_fcc(1, firdes.complex_band_pass(1, samp_rate, -TH/2 - transition_bw  ,TH/2 + transition_bw, transition_bw), ((TH)*2/3), samp_rate)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, vco_sens, 0.5)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_threshold_ff_0_1_0 = blocks.threshold_ff(0.25, 0.75, 0)
        self.blocks_threshold_ff_0_1 = blocks.threshold_ff(1.25, 1.75, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(2.25, 2.75, 0)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, int(interp))
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(int(math.log2(fsk)))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(3)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 124)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(3)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.5)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-20), 1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, int(samp_rate)))), True)
        self.analog_rail_ff_0_0 = analog.rail_ff((-1), 1)
        self.analog_rail_ff_0 = analog.rail_ff((-3), 3)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(((samp_rate*2)/(2*math.pi*TH) ))
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 2)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_rail_ff_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.analog_rail_ff_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_rail_ff_0_0, 0), (self.qtgui_time_sink_x_0_0, 3))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0_0, 2))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_threshold_ff_0_1, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_threshold_ff_0_1_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_threshold_ff_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_threshold_ff_0_1, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.blocks_threshold_ff_0_1_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.freq_xlating_fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.qtgui_freq_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK_4")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_spec_eff(self):
        return self.spec_eff

    def set_spec_eff(self, spec_eff):
        self.spec_eff = spec_eff
        self.set_TH(self.bw*self.spec_eff)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_TH(self.bw*self.spec_eff)

    def get_fsk(self):
        return self.fsk

    def set_fsk(self, fsk):
        self.fsk = fsk
        self.set_vco_sens(2*math.pi*self.TH/(self.fsk-1))

    def get_TH(self):
        return self.TH

    def set_TH(self, TH):
        self.TH = TH
        self.set_vco_sens(2*math.pi*self.TH/(self.fsk-1))
        self.analog_quadrature_demod_cf_0.set_gain(((self.samp_rate*2)/(2*math.pi*self.TH) ))
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.TH/2 - self.transition_bw  ,self.TH/2 + self.transition_bw, self.transition_bw))
        self.freq_xlating_fir_filter_xxx_0_0_0.set_center_freq(((self.TH)*2/3))

    def get_vco_sens(self):
        return self.vco_sens

    def set_vco_sens(self, vco_sens):
        self.vco_sens = vco_sens

    def get_variable_0_0(self):
        return self.variable_0_0

    def set_variable_0_0(self, variable_0_0):
        self.variable_0_0 = variable_0_0

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        self.transition_bw = transition_bw
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.TH/2 - self.transition_bw  ,self.TH/2 + self.transition_bw, self.transition_bw))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain(((self.samp_rate*2)/(2*math.pi*self.TH) ))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -self.TH/2 - self.transition_bw  ,self.TH/2 + self.transition_bw, self.transition_bw))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.blocks_repeat_0.set_interpolation(int(self.interp))




def main(top_block_cls=FSK_4, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
