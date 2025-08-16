class AuthController < ApplicationController
  include ActionController::Cookies

  def github
    info = request.env["omniauth.auth"]

    payload = {
      sub: info&.dig("uid"),
      email: info&.dig("info", "email"),
      iat: Time.now.to_i,
      exp: 30.minutes.from_now.to_i
    }

    token = jwt_encode(payload)

    cookies.encrypted[:access_token] = {
      value: token,
      httponly: true,
      secure: Rails.env.production?,
      expires: 30.minutes.from_now,
      same_site: :lax
    }

    redirect_to "#{frontend_url}/"
  end

  def failure
    render json: { ok: false, error: params[:message] }, status: :unauthorized
  end

  private

  def jwt_encode(payload)
    JWT.encode(payload, jwt_secret, "HS256")
  end

  def jwt_secret
    ENV.fetch("JWT_SECRET").presence || raise("JWT_SECRET environment variable is empty")
  end

  def frontend_url
    ENV.fetch("FRONTEND_URL")
  end
end
