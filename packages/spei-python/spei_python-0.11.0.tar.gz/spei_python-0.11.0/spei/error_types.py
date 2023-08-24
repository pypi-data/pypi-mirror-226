from enum import Enum


class NombreOrdenanteCodigoError(str, Enum):
    requerido = 11
    excede_longitud = 12
    invalido = 13
    vacio = 14


class TipoCuentaOrdenanteCodigoError(str, Enum):
    requerido = 15
    invalido = 16


class CuentaOrdenanteCodigoError(str, Enum):
    requerida = 17
    solo_digitos = 18
    excede_longitud = 19
    solo_ceros = 20
    clabe_longitud_incorrecta = 21
    tarjeta_longitud_incorrecta = 22


class CuentaOrdenanteIdentificacionCodigoError(str, Enum):
    invalida = 23
    excede_longitud = 24
    caracteres_invalidos = 25
    vacio = 26


class NombreBeneficiarioCodigoError(str, Enum):
    requerido = 27
    excede_longitud = 28
    caracters_invalidos = 29
    vacio = 30


class TipoCuentaBeneficiarioCodigoError(str, Enum):
    requerido = 31
    invalido = 32


class CuentaBeneficiarioCodigoError(str, Enum):
    requerida = 33
    solo_digitos = 34
    excede_longitud = 35
    solo_ceros = 36
    clabe_longitud_incorrecta = 37
    tarjeta_longitud_incorrecta = 38


class IdentificacionBeneficiarioCodigoError(str, Enum):
    invalida = 39
    excede_longitud = 40
    caracteres_invalidos = 41
    vacio = 42


class ConceptoCodigoError(str, Enum):
    concepto_requerido = 43
    concepto_excede_longitud = 44
    concepto_invalido = 45
    concepto_vacio = 46


class IvaCodigoError(str, Enum):
    iva_requerido = 47
    iva_mayor_a_cero = 48
    iva_menor_a_maximo = 49  # 9999999999999999.99


class ReferenciaCodigoError(str, Enum):
    referencia_requerida = 50
    referencia_mayor_a_cero = 51
    referencia_excede_longitud = 52


class ReferenciaCobranzaCodigoError(str, Enum):
    requerida = 53
    invalida = 54
    excede_longitud = 55
    solo_ceros = 56


class ClavePagoCodigoError(str, Enum):
    requerida = 57
    excede_longitud = 58
    invalida = 59
    vacia = 60


class NombreBeneficiario2CodigoError(str, Enum):
    requerido = 61
    excede_longitud = 62
    caracters_invalidos = 63
    vacio = 64


class TipoCuentaBeneficiario2CodigoError(str, Enum):
    requerido = 65
    invalido = 66


class CuentaBeneficiario2CodigoError(str, Enum):
    requerida = 67
    solo_digitos = 68
    excede_longitud = 69
    solo_ceros = 70
    clabe_longitud_incorrecta = 71
    ctarjeta_longitud_incorrecta = 72


class IdentificacionBeneficiario2CodigoError(str, Enum):
    invalida = 73
    excede_longitud = 74
    caracteres_invalidos = 75
    vacio = 76


class Concepto2CodigoError(str, Enum):
    concepto_requerido = 77
    concepto_excede_longitud = 78
    concepto_invalido = 79
    concepto_vacio = 80


class TipoOperacionCodigoError(str, Enum):
    requerido = 81
    invalido = 82


class MedioEntregaCodigoError(str, Enum):
    requerido = 83
    invalido = 84


class PrioridadCodigoError(str, Enum):
    requerido = 85
    invalido = 86


class TopologiaCodigoError(str, Enum):
    requerido = 87
    invalido = 88


class ClaveRastreoCodigoError(str, Enum):
    excede_longitud = 89
    invalido = 90
    vacio = 91
    requerida = 92


class OtrosCodigoError(str, Enum):
    fecha_operacion_requerido = 93
    tipo_traspaso_requerido = 94
    tipo_traspaso_invalido = 95
    medio_entrega_vacio = 96
    usuario_captura_requerido = 97
    estado_envio_requerido = 98
    estado_envio_invalido = 99
    clave_rastreo_existente = 100
    usuario_no_existe = 101
    causa_devolucion_invalida = 102
    causa_devolucion_requerida = 103
    fecha_operacion_fecha_invalida = 104
    fecha_operacion_hora_invalida = 105
    tipo_orden_requerido = 106
    tipo_orden_invalido = 107
    fecha_operacion_invalida = 108  # yyyyMMdd
    op_folio_invalido = 109  # -1
    op_folio_invalido_2 = 110  # -1
    fecha_operacion_incorrecta = 111  # debe ser la del sistema karpay
    cuenta_beneficiario_2_requerida = 112
    tipo_cuenta_beneficiario_2_requerida = 113
    devolucion_sin_correspondencia = 114
    tipo_pago_invalido = 115
    tipo_cuenta_celular_cuenta_ordenante_invalida = 116  # 10 digitos
    tipo_cuenta_celular_cuenta_beneficiario_invalida = 117  # 10 digitos
    cde_vacio = 118
    cde_requerido = 119
    usuario_autorizado_requerido_traspasos = 120
    tipo_pago_horario_invalido = 121
    tipo_pago_cuenta_beneficiario_invalido = 122
    operaciones_concluidas = 123
    tipo_cuenta_ordenante_requerido = 124
    tipo_cuenta_beneficiario_requerida = 125
    cuenta_beneficiario_2_invalida = 126
    tipo_de_pago_invalido = 127
    cuenta_clabe_invalida = 175
    usuario_no_pertenece_empresa = -20
    tipo_cuenta_ordenante_no_habilitado_habiles = -21
    tipo_cuenta_ordenante_no_habilitado_inhabiles = -22
    tipo_cuenta_ordenante_fuera_horario_habiles = -23
    tipo_cuenta_ordenante_fuera_horario_inhabiles = -24
    tipo_cuenta_beneficiario_no_habilitado_habiles = -25
    tipo_cuenta_beneficiario_no_habilitado_inhabiles = -26
    tipo_cuenta_beneficiario_fuera_horario_habiles = -27
    tipo_cuenta_beneficiario_fuera_horario_inhabiles = -28
    tipo_cuenta_beneficiario_2_no_habilitado_habiles = -29
    tipo_cuenta_beneficiario_2_no_habilitado_inhabiles = -30
    tipo_cuenta_beneficiario_2_fuera_horario_habiles = -31
    tipo_cuenta_beneficiario_2_fuera_horario_inhabiles = -32
    cuenta_ordenante_no_pertence_banxico = -33
    tipo_pago_invalido_coa_poa = -34
    institucion_no_certificada_poa = -35
    cuenta_ordenante_domicilio_requerido = 128
    cuenta_ordenante_domicilio_excede_longitud = 129
    cuenta_ordenante_domicilio_invalido = 130
    cuenta_ordenante_domicilio_vacio = 131


class CodigoPostalOrdenante(str, Enum):
    requerido = 132
    numerico = 133
    excede_longitud = 134
    vacio = 135


class FechaConstitucionOrdenante(str, Enum):
    requerido = 136
    excede_longitud = 137
    invalida = 138


class DevolucionExtemporaneaCodigoError(str, Enum):
    clave_rastreo_requerido = 400
    clave_rastreo_excede_longitud = 401
    clave_rastreo_invalida = 402
    folio_paquete_longitud_incorrecta = 403
    folio_paquete_numerico = 404
    folio_paquete_vacio = 405
    folio_pago_longitud_incorrecta = 406
    folio_pago_solo_numeros = 407
    folio_pago_vacio = 409
    fecha_operacion_original_requerida = 410
    fecha_operacion_original_longitud_incorrecta = 411
    interes_original_requerido = 412
    interes_original_longitud_incorrecta = 413
    interes_original_invalido = 414
    interes_original_no_permitido = 415
    monto_original_requerido = 416
    monto_original_longitud_incorrecta = 417
    monto_original_invalido = 418
    monto_original_no_permitido = 419
    clave_rastreo_hexadecimal_requerido = 420
    clave_rastreo_hexadecimal_longitud_incorrecta = 421


class ClasificacionOperacionCodigoError(str, Enum):
    requerido = 139
    excede_longitud = 140
    solo_numerica = 141
    invalido = 142


class DireccionIPCodigoError(str, Enum):
    requerido = 143
    excede_longitud = 144
    invalida = 145


class FechaInstruccionCodigoError(str, Enum):
    requerida = 146
    excede_longitud = 147
    invalido = 148


class HoraInstruccionCodigoError(str, Enum):
    requerida = 149
    excede_longitud = 150
    invalido = 151


class FechaAceptacionCodigoError(str, Enum):
    requerida = 152
    excede_longitud = 153
    invalido = 154


class HoraAceptacionCodigoError(str, Enum):
    requerida = 155
    excede_longitud = 156
    invalido = 157


class ClaveBancoUsuarioCodigoError(str, Enum):
    requerida = 158
    numerica = 159
    excede_longitud = 160
    solo_ceros = 161


class TipoCuentaBancoUsuarioCodigoError(str, Enum):
    requerido = 162
    invalida = 163


class BancoUsuarioCodigoError(str, Enum):
    requerido = 164
    numerica = 165
    excede_longitud = 166
    solo_ceros = 167
    tipo_cuenta_clabe_invalida = 168
    tipo_cuenta_tarjeta_invalida = 169
    primeros_digitos_incorrectos = 172  # [1,2]
    fiel_invalida = 173
    cuenta_inexistente = 174
    tipo_cuenta_clabe_cuenta_ordenante_incorrecta = 422  # no pertenece al participante
    digito_verificador_incorrecto = 423
    monto_original_incorrecto = 424  # no coincide monto menos el interes
    # no es posible una devolucion de una devolucion extratemporanea  noqa:E501
    devolucion_extratemporanea_no_permitida = 425
    devolucion_extratemporanea_fecha_incorrecta = 426
    devolucion_no_permitida = 427  # no es posible una devolucion de una devolucion


class PagoFacturaCodigoError(str, Enum):
    requerido = 428
    excede_longitud = 429
    invalida = 430
    incorrecto = 431
    faltan_datos = 432
    uuid_invalido = 433
    importe_invalido = 434
    excede_numero = 435
    tipo_pago_invalido = 188
    firma_invalida = 436
    certificado_no_encontrado = 437
    sistema_no_disponible = 441
    listener_outgoing_no_habilitado = 500


class CoDiCodigoError(str, Enum):
    certificado_invalido = 442
    certificado_requerido = 443
    certificado_excede_longitud = 444
    folio_codi_requerido = 445
    folio_codi_invalido = 446
    folio_codi_excede_longitud = 447
    pago_comision_requerido = 448
    pago_comision_invalido = 449
    pago_comision_numero = 450
    monto_comision_requerido = 451
    monto_comision_invalido = 452
    telefono_ordenante_numerico = 453
    telefono_ordenante_requerido = 454
    telefono_ordenante_invalido = 455
    telefono_ordenante_excede_longitud = 456
    digito_verificador_ordenante_numerico = 457
    digito_verificador_ordenante_requerido = 458
    digito_verificador_ordenante_invalido = 459
    digito_verificador_ordenante_excede_longitud = 460
    telefono_beneficiario_numerico = 461
    telefono_beneficiario_requerido = 462
    telefono_beneficiario_invalido = 463
    telefono_beneficiario_excede_longitud = 464
    digito_verificador_beneficiario_numerico = 465
    digito_verificador_beneficiario_requerido = 466
    digito_verificador_beneficiario_invalido = 467
    digito_verificador_beneficiario_excede_longitud = 468
    digito_verificador_comercio_alfanumerico = 469
    digito_verificador_comercio_requerido = 470
    digito_verificador_comercio_excede_longitud = 471


class DevolucionAcreditadaCodigoError(str, Enum):
    no_encontrada = 472
    devolucion_no_permitida = 473
    institucion_incorrecta = 474
    orden_no_liquidada = 475
    fecha_operacion_incorrecta = 476  # es la misma que la fecha de operación actual
    abono_no_encontrado = 477
    no_permitida = 478
    ya_devuelta = 479
    orden_no_liquidada_banxico = 480
    # no puede ser mayor al de la orden original
    devolucion_tipo_pago_codi_monto_incorrecto = 481
    monto_superior_original = 482   # no puede ser superior al original
    monto_incorrecto = 483
