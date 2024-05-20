#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: acm_phy_layer
# Author: Ckjaer
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from g4fsk_decoding import g4fsk_decoding  # grc-generated hier_block
from gnuradio import analog
import math
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import numpy as np
import physical_layer_transmitter_epy_block_0 as epy_block_0  # embedded python block
import physical_layer_transmitter_epy_block_0_0 as epy_block_0_0  # embedded python block
import physical_layer_transmitter_epy_block_0_0_0 as epy_block_0_0_0  # embedded python block
import physical_layer_transmitter_epy_block_0_1 as epy_block_0_1  # embedded python block
import physical_layer_transmitter_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import physical_layer_transmitter_epy_block_1_0_0_0 as epy_block_1_0_0_0  # embedded python block
import physical_layer_transmitter_epy_block_2_0 as epy_block_2_0  # embedded python block
import physical_layer_transmitter_taps as taps  # embedded python module
import physical_layer_transmitter_th as th  # embedded python module
import sip



class physical_layer_transmitter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "acm_phy_layer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("acm_phy_layer")
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

        self.settings = Qt.QSettings("GNU Radio", "physical_layer_transmitter")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e3
        self.bandwidth = bandwidth = 25000
        self.repack_size = repack_size = 1
        self.interpolation = interpolation = int(np.ceil(samp_rate/(th.modcod(bandwidth, "1"))))
        self.bp_filter_0 = bp_filter_0 = firdes.complex_band_pass(1.0, samp_rate, -bandwidth/2 - 200, bandwidth/2 + 200, 200, window.WIN_RECTANGULAR, 6.76)
        self.bp_filter = bp_filter = firdes.complex_band_pass(1.0, samp_rate, -th.modcod(bandwidth, "7")/2 - 200, th.modcod(bandwidth, "7")/2 + 200, 200, window.WIN_RECTANGULAR, 6.76)

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://localhost:5555', 100, False)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://*:5556', 100, True)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
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
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_fff(1, taps.generate_taps(4, 0.25))
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(1, taps.generate_taps(4, 0.25))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.g4fsk_decoding_0 = g4fsk_decoding(
            movav=30,
        )
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, bp_filter_0, (bandwidth*2/3 + 200), samp_rate)
        self.epy_block_2_0 = epy_block_2_0.blk(fft_size=2**15, bandwidth=25e3, samplerate=samp_rate, addr="snr_meas")
        self.epy_block_1_0_0_0 = epy_block_1_0_0_0.blk(addr='demux_1')
        self.epy_block_1_0_0 = epy_block_1_0_0.blk(addr='mux_1')
        self.epy_block_0_1 = epy_block_0_1.blk()
        self.epy_block_0_0_0 = epy_block_0_0_0.blk(snr=20, addr="awgn")
        self.epy_block_0_0 = epy_block_0_0.blk(addr='demux')
        self.epy_block_0 = epy_block_0.blk(addr='mux', interpolation=int(np.ceil(samp_rate/(th.modcod(bandwidth, "1")))), samp_rate=samp_rate, bandwidth=bandwidth)
        self.digital_symbol_sync_xx_1_0_0_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            interpolation,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_symbol_sync_xx_1_0_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            interpolation,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_symbol_sync_xx_1_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            interpolation,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bf([-1.5, -0.5, 0.5, 1.5], 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bf([-1, 1], 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1, 1], 1)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vco_f_1 = blocks.vco_f(samp_rate, (2*np.pi*bandwidth/3), 0.5)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (2**15))
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(repack_size, gr.GR_MSB_FIRST)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_interpolation)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_repack_size)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_quadrature_demod_cf_2 = analog.quadrature_demod_cf((samp_rate*2/(2*np.pi*bandwidth)))
        self.analog_quadrature_demod_cf_1 = analog.quadrature_demod_cf(1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc(((np.pi / 2) / 4))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(((np.pi / 2) / 4))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'repack_out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'interp_out'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_1_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_1_0_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_2_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_1_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_1_0_0_0, 'msg_in'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.epy_block_1_0_0, 2))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.epy_block_1_0_0, 1))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_symbol_sync_xx_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_1, 0), (self.digital_symbol_sync_xx_1_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_2, 0), (self.digital_symbol_sync_xx_1_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.epy_block_1_0_0_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_vco_f_1, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.epy_block_1_0_0_0, 2))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.epy_block_1_0_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0_0_0, 0), (self.g4fsk_decoding_0, 0))
        self.connect((self.epy_block_0, 2), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.epy_block_0, 1), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.epy_block_0_0, 2), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.epy_block_0_0, 1), (self.analog_quadrature_demod_cf_1, 0))
        self.connect((self.epy_block_0_0, 0), (self.analog_quadrature_demod_cf_2, 0))
        self.connect((self.epy_block_0_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_0_0_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.epy_block_0_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.epy_block_0_1, 0), (self.blocks_vco_f_1, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_0_0_0, 0))
        self.connect((self.epy_block_1_0_0_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.epy_block_1_0_0, 0))
        self.connect((self.g4fsk_decoding_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.epy_block_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "physical_layer_transmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bp_filter(firdes.complex_band_pass(1.0, self.samp_rate, -th.modcod(self.bandwidth, "7")/2 - 200, th.modcod(self.bandwidth, "7")/2 + 200, 200, window.WIN_RECTANGULAR, 6.76))
        self.set_bp_filter_0(firdes.complex_band_pass(1.0, self.samp_rate, -self.bandwidth/2 - 200, self.bandwidth/2 + 200, 200, window.WIN_RECTANGULAR, 6.76))
        self.set_interpolation(int(np.ceil(self.samp_rate/(th.modcod(self.bandwidth, "1")))))
        self.analog_quadrature_demod_cf_2.set_gain((self.samp_rate*2/(2*np.pi*self.bandwidth)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.epy_block_0.samp_rate = self.samp_rate
        self.epy_block_2_0.samplerate = self.samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_bp_filter(firdes.complex_band_pass(1.0, self.samp_rate, -th.modcod(self.bandwidth, "7")/2 - 200, th.modcod(self.bandwidth, "7")/2 + 200, 200, window.WIN_RECTANGULAR, 6.76))
        self.set_bp_filter_0(firdes.complex_band_pass(1.0, self.samp_rate, -self.bandwidth/2 - 200, self.bandwidth/2 + 200, 200, window.WIN_RECTANGULAR, 6.76))
        self.set_interpolation(int(np.ceil(self.samp_rate/(th.modcod(self.bandwidth, "1")))))
        self.analog_quadrature_demod_cf_2.set_gain((self.samp_rate*2/(2*np.pi*self.bandwidth)))
        self.epy_block_0.bandwidth = self.bandwidth
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.bandwidth*2/3 + 200))

    def get_repack_size(self):
        return self.repack_size

    def set_repack_size(self, repack_size):
        self.repack_size = repack_size

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.digital_symbol_sync_xx_1_0.set_sps(self.interpolation)
        self.digital_symbol_sync_xx_1_0_0.set_sps(self.interpolation)
        self.digital_symbol_sync_xx_1_0_0_0.set_sps(self.interpolation)

    def get_bp_filter_0(self):
        return self.bp_filter_0

    def set_bp_filter_0(self, bp_filter_0):
        self.bp_filter_0 = bp_filter_0
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.bp_filter_0)

    def get_bp_filter(self):
        return self.bp_filter

    def set_bp_filter(self, bp_filter):
        self.bp_filter = bp_filter




def main(top_block_cls=physical_layer_transmitter, options=None):

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
